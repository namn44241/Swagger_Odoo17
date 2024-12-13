/** @odoo-module */

const SwaggerUI = {
    init(selector) {
        this.selector = selector;
        this.$el = $(this.selector);
        this.start();
    },

    _swagger_bundle_settings() {
        const defaults = {
            dom_id: this.selector,
            deepLinking: true,
            presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
            plugins: [SwaggerUIBundle.plugins.DownloadUrl],
            layout: "StandaloneLayout",
            operationsSorter: function (a, b) {
                var methodsOrder = [
                    "get",
                    "post",
                    "put",
                    "delete",
                    "patch",
                    "options",
                    "trace",
                ];
                var result =
                    methodsOrder.indexOf(a.get("method")) -
                    methodsOrder.indexOf(b.get("method"));
                if (result === 0) {
                    result = a.get("path").localeCompare(b.get("path"));
                }
                return result;
            },
            tagsSorter: "alpha",
            onComplete: function () {
                if (this.web_btn === undefined) {
                    this.web_btn = $(
                        "<a class='fa fa-th-large swg-odoo-web-btn' href='/web' accesskey='h'></a>"
                    );
                    $(".topbar").prepend(this.web_btn);
                }
            },
            oauth2RedirectUrl:
                window.location.origin +
                "/base_rest/static/lib/swagger-ui-3.51.1/oauth2-redirect.html",
        };
        const config = this.$el.data("settings");
        return Object.assign({}, defaults, config);
    },

    start() {
        this.ui = SwaggerUIBundle(this._swagger_bundle_settings());
    },
};

// Initialize when DOM is ready
$(document).ready(() => {
    SwaggerUI.init("#swagger-ui");
});
