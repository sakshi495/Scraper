JS_CODE = ["""
(() => {
    window.scrollTo(0, document.body.scrollHeight * 0.3);
    setTimeout(() => {
        window.scrollTo(0, document.body.scrollHeight * 0.6);
        setTimeout(() => {
            window.scrollTo(0, document.body.scrollHeight);
            document.querySelectorAll('.show-more-btn, .expand-btn, .more-btn, .view-more, [class*=expand], [class*=more]')
                    .forEach(btn => btn.click());
            document.querySelectorAll('.tab-title:not(.active), .tab:not(.active), .nav-item:not(.active)')
                    .forEach(tab => {
                const label = tab.textContent.toLowerCase();
                if (label.includes('spec') || label.includes('attribute') || label.includes('detail')) tab.click();
            });
            setTimeout(() => { window.scrollTo(0, 0); }, 1000);
        }, 1500);
    }, 1000);
})();
"""]
