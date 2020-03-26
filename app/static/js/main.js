var App = {
    init: function() {
        App.bindUI();
    },

    components: {
        btnConvert: $("#btn-convert"),
        btnClear: $("#btn-clear"),
        btnCopy: $("#btn-copy"),
        btnHelp: $("#btn-help"),
        btnHelpClose: $(".btn-help-close"),
        btnReaderView: $("#btn-reader-view"),
        btnReaderViewClose: $(".btn-reader-view-close"),
        txtInputRecipe: $("#input-recipe"),
        txtInputMultiplier: $("#input-multiplier"),
        txtReaderView: $("#reader-view-content"),
        txtOutputRecipe: $("#output-recipe"),
        modalReaderView: $("#reader-view"),
        modalHelp: $("#modal-help")
    },

    routes: {
        convert: "convert",
        ingredientFromUrl: "ingredients_from_url"
    },

    bindUI: function() {
        App.components.btnConvert.on("click", App.onConvertClicked);
        App.components.btnClear.on("click", App.onClearClicked);
        App.components.btnCopy.on("click", App.onCopyClicked);
        App.components.btnHelp.on("click", App.onHelpClicked);
        App.components.btnHelpClose.on("click", App.onHelpCloseClicked);
        App.components.btnReaderView.on("click", App.onReaderViewClicked);
        App.components.btnReaderViewClose.on("click", App.onReaderViewCloseClicked);
    },

    convertRecipe: function(recipe, multiplier) {
        return $.post(
            App.routes.convert,
            { "data": recipe, "multiplier": multiplier },
            function (data) {
                App.components.txtOutputRecipe.val(data);
            }
        );
    },

    appendInstructions: function(instructions) {
        App.components.txtOutputRecipe.val(function () {
            return this.value + "\n\n" + instructions;
        })
    },

    onConvertClicked: function() {
        if (App.components.txtInputRecipe.val().includes("http")) {
            App.components.btnConvert.prop("disabled", true);
            App.components.btnClear.prop("disabled", true);

            // Get ingredients from URL, then convert
            $.post(App.routes.ingredientFromUrl, { "url": App.components.txtInputRecipe.val() },
                function (data) {
                    App.components.txtInputRecipe.val(data["ingredients"])
                    App.convertRecipe(
                        data["ingredients"], App.components.txtInputMultiplier.val()
                    ).done(function() {
                        App.appendInstructions(data["instructions"])
                    })
            }).fail(function () {
                alert("Parsing error: Website not supported for " + App.components.txtInputRecipe.val() + "\n\nPlease manually copy the recipe into the input box.")
            }).always(function () {
                App.components.btnConvert.prop("disabled", false);
                App.components.btnClear.prop("disabled", false);
            })
        }
        else {
            var split_str = App.components.txtInputRecipe.val().split("\n\n\n")

            var ingredients = split_str[0]
            var instructions = split_str[1]

            console.debug(ingredients)
            console.debug(instructions)

            // Ingredients entered manually
            App.convertRecipe(
                ingredients, App.components.txtInputMultiplier.val()
            ).done(function() {
                App.appendInstructions(instructions.replace(/\n/g, "\n\n"))
            })
        }
    },

    onClearClicked: function() {
        App.components.txtInputRecipe.val("");
        App.components.txtInputRecipe.focus();
    },

    onCopyClicked: function() {
        copyToClipboard(App.components.txtOutputRecipe.val());
        new Toast({ message: 'Output recipe copied to clipboard!', type: 'success' });
    },

    onHelpClicked: function() {
        App.components.modalHelp.addClass("active");
    },

    onHelpCloseClicked: function() {
        App.components.modalHelp.removeClass("active");
    },

    onReaderViewClicked: function() {
        App.components.txtReaderView.text(App.components.txtOutputRecipe.val());
        App.components.modalReaderView.addClass("active")
    },

    onReaderViewCloseClicked: function() {
        App.components.modalReaderView.removeClass("active")
    },
}


// Copies a string to the clipboard. Must be called from within an
// event handler such as click. May return false if it failed, but
// this is not always possible. Browser support for Chrome 43+,
// Firefox 42+, Safari 10+, Edge and Internet Explorer 10+.
// Internet Explorer: The clipboard feature may be disabled by
// an administrator. By default a prompt is shown the first
// time the clipboard is used (per session).
function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
        return clipboardData.setData("Text", text);

    }
    else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        }
        catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        }
        finally {
            document.body.removeChild(textarea);
        }
    }
}

window.addEventListener("load", function () {
    App.init();
});
