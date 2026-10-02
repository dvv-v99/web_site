(function () {
    var toggle = document.querySelector('.nav-toggle');
    var panel = document.getElementById('mobile-nav');

    if (toggle && panel) {
        var setOpen = function (open) {
            toggle.classList.toggle('is-open', open);
            panel.classList.toggle('is-open', open);
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            document.body.style.overflow = open ? 'hidden' : '';
        };

        toggle.addEventListener('click', function () {
            setOpen(!panel.classList.contains('is-open'));
        });

        panel.addEventListener('click', function (event) {
            if (event.target.closest('a')) {
                setOpen(false);
            }
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                setOpen(false);
            }
        });

        window.addEventListener('resize', function () {
            if (window.innerWidth > 900) {
                setOpen(false);
            }
        });
    }

    var toTop = document.querySelector('[data-scroll-top]');

    if (toTop) {
        toTop.addEventListener('click', function (event) {
            event.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
})();