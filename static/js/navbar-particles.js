(async () => {
    await loadSlim(tsParticles);

    await tsParticles.load({
        id: "navbar-particles",
        options: {
            fullScreen: {
                enable: false
            },

            background: {
                color: {
                    value: "transparent"
                }
            },

            fpsLimit: 60,

            particles: {
                number: {
                    value: 20
                },

                color: {
                    value: "#ffffff"
                },

                opacity: {
                    value: 0.25
                },

                size: {
                    value: {
                        min: 3,
                        max: 8
                    }
                },

                shape: {
                    type: "circle"
                },

                move: {
                    enable: true,
                    speed: 1,
                    direction: "top",
                    outModes: {
                        default: "out"
                    }
                }
            },

            detectRetina: true
        }
    });
})();