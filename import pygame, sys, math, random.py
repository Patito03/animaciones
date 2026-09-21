<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Jardín Mágico 💛</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
        }
        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #03050b;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 1;
        }
        .btn-wrapper {
            position: absolute;
            bottom: 8%;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            transition: opacity 0.5s ease;
        }
        button, .wa-btn {
            background: rgba(255, 215, 0, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 215, 0, 0.3);
            color: #ffe55c;
            padding: 12px 30px;
            font-size: 0.9rem;
            font-weight: 500;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 240px;
        }
        button:hover, .wa-btn:hover {
            background: rgba(255, 215, 0, 0.2);
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        }
        .wa-btn {
            border-color: rgba(37, 211, 102, 0.5);
            color: #25d366;
            background: rgba(37, 211, 102, 0.12);
        }
        .wa-btn:hover {
            background: rgba(37, 211, 102, 0.25);
            box-shadow: 0 0 20px rgba(37, 211, 102, 0.4);
        }
        .fade-out {
            opacity: 0;
            pointer-events: none;
        }
    </style>
</head>
<body>

    <canvas id="canvas"></canvas>

    <div class="btn-wrapper" id="btnWrapper">
        <button id="actionBtn">Construir Ramo</button>
        <a id="waShareBtn" class="wa-btn" href="#" target="_blank">Enviar por WhatsApp</a>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const actionBtn = document.getElementById('actionBtn');
        const btnWrapper = document.getElementById('btnWrapper');
        const waShareBtn = document.getElementById('waShareBtn');

        // --- CONFIGURACIÓN ---
        // 1. Sube tu archivo .html a GitHub Gist (gist.github.com)
        // 2. Haz clic en el botón "Raw" de tu Gist y copia la URL
        // 3. Pega esa URL aquí abajo entre las comillas:
        const enlacePagina = "AQUÍ_DEBES_PEGAR_EL_LINK_DE_TU_GIST_RAW";
        // ----------------------

        const mensajeBase = "¡Hola! Te comparto este jardín mágico interactivo con mariposas reales que arman un ramo de flores 💛. ¡Míralo aquí: ";
        const mensajeWhatsApp = encodeURIComponent(mensajeBase + enlacePagina);
        waShareBtn.href = `https://api.whatsapp.com/send?text=${mensajeWhatsApp}`;

        let width, height;
        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        let state = 'IDLE';
        let animationProgress = 0;
        let particles = [];
        let fireflies = [];

        const colors = [
            { primary: '#ff3366', dark: '#800f2f', glow: '#ff758f' },
            { primary: '#00b4d8', dark: '#03045e', glow: '#90e0ef' },
            { primary: '#7209b7', dark: '#3a0ca3', glow: '#b5179e' },
            { primary: '#ffb703', dark: '#d48c08', glow: '#ffd166' },
            { primary: '#2ec4b6', dark: '#014f86', glow: '#cbf3f0' }
        ];

        const flowerPositions = [
            {x: 0, y: -40},    // 0: Flor central
            {x: -45, y: -5},   // 1: Izquierda
            {x: 45, y: -5},    // 2: Derecha
            {x: -25, y: -80},  // 3: Arriba Izq
            {x: 25, y: -80},   // 4: Arriba Der
            {x: 0, y: -110}    // 5: Arriba
        ];

        let butterflies = [];
        for (let i = 0; i < 20; i++) {
            let isBuilder = i < flowerPositions.length;
            butterflies.push({
                x: Math.random() * width,
                y: Math.random() * height,
                targetX: 0,
                targetY: 0,
                freeAngle: Math.random() * Math.PI * 2,
                size: Math.random() * 12 + 40,
                speed: Math.random() * 2.5 + 2.0,
                wingSpeed: Math.random() * 0.25 + 0.18,
                offset: Math.random() * 100,
                colorObj: colors[Math.floor(Math.random() * colors.length)],
                isBuilder: isBuilder,
                flowerIndex: isBuilder ? i : -1,
                hasDelivered: false
            });
        }

        for(let i = 0; i < 60; i++) {
            fireflies.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.5 + 0.5,
                alpha: Math.random() * 0.5,
                speed: Math.random() * 0.02,
                angle: Math.random() * Math.PI * 2
            });
        }

        window.addEventListener('pointerdown', (e) => {
            const x = e.clientX;
            const y = e.clientY;
            for (let i = 0; i < 6; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 5,
                    vy: (Math.random() - 1) * -3 - 1,
                    size: Math.random() * 8 + 4,
                    alpha: 1,
                    decay: Math.random() * 0.015 + 0.01,
                    color: colors[Math.floor(Math.random() * colors.length)].glow,
                    isHeart: true
                });
            }
        });

        actionBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (state === 'IDLE' || state === 'COMPLETED') {
                state = 'BUILDING';
                animationProgress = 0;
                btnWrapper.classList.add('fade-out');

                const centerX = width / 2;
                const centerY = height / 2 + 50;

                butterflies.forEach((b) => {
                    b.hasDelivered = false;
                    if (b.isBuilder) {
                        let pos = flowerPositions[b.flowerIndex];
                        b.targetX = centerX + pos.x * 2.5;
                        b.targetY = centerY + pos.y * 2.5;
                    }
                });
            }
        });

        function spawnSnapParticles(x, y, color) {
            for (let i = 0; i < 8; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 6,
                    vy: (Math.random() - 0.5) * 6,
                    size: Math.random() * 4 + 2,
                    alpha: 1,
                    decay: 0.03,
                    color: color,
                    isHeart: false
                });
            }
        }

        function drawButterflyShape(ctx, x, y, size, colorObj, wingScale) {
            ctx.save();
            ctx.translate(x, y);
            ctx.shadowBlur = 18;
            ctx.shadowColor = colorObj.glow;

            ctx.save();
            ctx.scale(Math.abs(wingScale), 1);
            
            let wingGrad = ctx.createLinearGradient(0, -size, 0, 0);
            wingGrad.addColorStop(0, colorObj.primary);
            wingGrad.addColorStop(1, colorObj.dark);
            ctx.fillStyle = wingGrad;

            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(-size * 0.4, -size * 0.2, -size * 1.4, -size * 0.9, -size * 1.2, -size * 0.4);
            ctx.bezierCurveTo(-size * 1.0, -size * 0.1, -size * 0.4, size * 0.1, 0, 0);
            ctx.fill();

            ctx.fillStyle = '#ffffff';
            ctx.globalAlpha = 0.8;
            ctx.beginPath();
            ctx.arc(-size * 0.7, -size * 0.4, size * 0.12, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(-size * 0.9, -size * 0.3, size * 0.07, 0, Math.PI * 2);
            ctx.fill();
            ctx.globalAlpha = 1.0;

            ctx.fillStyle = wingGrad;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(size * 0.4, -size * 0.2, size * 1.4, -size * 0.9, size * 1.2, -size * 0.4);
            ctx.bezierCurveTo(size * 1.0, -size * 0.1, size * 0.4, size * 0.1, 0, 0);
            ctx.fill();

            ctx.fillStyle = '#ffffff';
            ctx.globalAlpha = 0.8;
            ctx.beginPath();
            ctx.arc(size * 0.7, -size * 0.4, size * 0.12, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(size * 0.9, -size * 0.3, size * 0.07, 0, Math.PI * 2);
            ctx.fill();
            ctx.globalAlpha = 1.0;
            ctx.restore();

            ctx.save();
            ctx.scale(Math.abs(wingScale), 1);
            ctx.fillStyle = colorObj.primary;
            
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(-size * 0.3, size * 0.1, -size * 1.0, size * 0.4, -size * 0.8, size * 0.9);
            ctx.bezierCurveTo(-size * 0.5, size * 1.0, -size * 0.1, size * 0.5, 0, 0);
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(size * 0.3, size * 0.1, size * 1.0, size * 0.4, size * 0.8, size * 0.9);
            ctx.bezierCurveTo(size * 0.5, size * 1.0, size * 0.1, size * 0.5, 0, 0);
            ctx.fill();
            ctx.restore();

            ctx.fillStyle = '#111111';
            ctx.beginPath();
            ctx.ellipse(0, 0, size * 0.08, size * 0.5, 0, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = '#111111';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(0, -size * 0.45);
            ctx.quadraticCurveTo(-size * 0.25, -size * 0.75
