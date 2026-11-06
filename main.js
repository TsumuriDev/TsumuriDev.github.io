/**
 * TSUMURI19 & ZOEMC NETWORK — Interactive Script
 * Style inspired by vedal.ai
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. One-Click Copy IP to Clipboard with Animated Toast
    const copyBtns = document.querySelectorAll('.copy-ip-btn');
    const toast = document.getElementById('copy-toast');
    let toastTimeout;

    copyBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const ip = btn.getAttribute('data-ip') || 'zoemc.online';

            try {
                await navigator.clipboard.writeText(ip);
                showToast(`Đã sao chép IP máy chủ: <strong>${ip}</strong>! Sẵn sàng vào game! 🎮`);
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = ip;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                try {
                    document.execCommand('copy');
                    showToast(`Đã sao chép IP: <strong>${ip}</strong>! 🎮`);
                } catch (fallbackErr) {
                    showToast(`IP Máy chủ ZoeMC: <strong>${ip}</strong>`);
                }
                document.body.removeChild(textArea);
            }
        });
    });

    function showToast(htmlMessage) {
        if (!toast) return;
        toast.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>${htmlMessage}</span>`;
        toast.classList.add('show');

        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, 2800);
    }

    // 2. Interactive BGM Music Player
    const bgmAudio = document.getElementById('bgm-audio');
    const musicPlayer = document.getElementById('music-player');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const playIcon = document.getElementById('play-icon');
    const musicDisc = document.getElementById('music-disc');
    const musicLabel = document.getElementById('music-label');
    const muteBtn = document.getElementById('mute-btn');
    const volIcon = document.getElementById('vol-icon');

    if (bgmAudio && musicPlayer) {
        // Set comfortable background volume (35%)
        bgmAudio.volume = 0.35;

        const togglePlay = async () => {
            if (bgmAudio.paused) {
                try {
                    await bgmAudio.play();
                    musicPlayer.classList.add('playing');
                    playIcon.className = 'fa-solid fa-pause';
                    if (musicLabel) musicLabel.textContent = 'BGM · ĐANG PHÁT';
                } catch (err) {
                    console.log('Autoplay restriction or audio error:', err);
                }
            } else {
                bgmAudio.pause();
                musicPlayer.classList.remove('playing');
                playIcon.className = 'fa-solid fa-play';
                if (musicLabel) musicLabel.textContent = 'BGM · TẮT';
            }
        };

        if (playPauseBtn) playPauseBtn.addEventListener('click', togglePlay);
        if (musicDisc) musicDisc.addEventListener('click', togglePlay);

        // Mute / Unmute
        if (muteBtn && volIcon) {
            muteBtn.addEventListener('click', () => {
                bgmAudio.muted = !bgmAudio.muted;
                if (bgmAudio.muted) {
                    volIcon.className = 'fa-solid fa-volume-xmark';
                    muteBtn.style.color = '#ef4444';
                } else {
                    volIcon.className = 'fa-solid fa-volume-high';
                    muteBtn.style.color = '';
                }
            });
        }
    }

    // 3. Mouse Parallax / 3D Tilt effect on Avatar Cards
    const avatarWrapper = document.querySelector('.avatar-card-wrapper');
    const heroVisual = document.querySelector('.hero-visual');

    if (heroVisual && avatarWrapper) {
        heroVisual.addEventListener('mousemove', (e) => {
            const rect = heroVisual.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            const rotateX = -(y / rect.height) * 16;
            const rotateY = (x / rect.width) * 16;

            avatarWrapper.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        heroVisual.addEventListener('mouseleave', () => {
            avatarWrapper.style.transform = `perspective(800px) rotateX(0deg) rotateY(0deg)`;
        });
    }

    // 4. Mouse spotlight glow tracking on cards
    const interactiveCards = document.querySelectorAll('.dest-card, .blog-feature, .spotlight-card, .mockup-frame, .vtuber-card-showcase');
    interactiveCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    // 5. Back to top button
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // 6. Console Greeting Easter Egg
    console.log(
        '%c🎮 TSUMURI19 (Nguyễn Văn Trường) %c\n🔨 ZOE STUDIO: https://discord.gg/wqcNG4YSBT (Mọi thứ về Minecraft)\n👾 ZoeMC Network: zoemc.online\n💻 GitHub: https://github.com/TsumuriDev\n💜 TikTok: @tsumuri.vtuber\n✨ Discord ZoeMC: https://discord.gg/Xc7ub3YtEC',
        'color: #EA10DE; font-size: 18px; font-weight: bold; background: #141118; padding: 8px 14px; border-radius: 8px; border: 1px solid #EA10DE;',
        'color: #44eb7e; font-size: 13px; line-height: 1.6;'
    );
});
