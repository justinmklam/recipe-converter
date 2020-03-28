"use strict";

var App = {
    components: {
        btnConvert: document.getElementById("btn-convert"),
        btnClear: document.getElementById("btn-clear"),
        btnCopy: document.getElementById("btn-copy"),
        btnHelp: document.getElementById("btn-help"),
        btnHelpClose: document.querySelectorAll(".btn-help-close"),
        btnReaderView: document.getElementById("btn-reader-view"),
        btnReaderViewClose: document.querySelectorAll(".btn-reader-view-close"),
        txtInputRecipe: document.getElementById("input-recipe"),
        txtInputMultiplier: document.getElementById("input-multiplier"),
        txtReaderView: document.getElementById("reader-view-content"),
        txtOutputRecipe: document.getElementById("output-recipe"),
        modalReaderView: document.getElementById("reader-view"),
        modalHelp: document.getElementById("modal-help")
    },

    routes: {
        convert: "convert",
        ingredientFromUrl: "ingredients_from_url"
    },

    init: function() {
        App.addEventListeners();
    },

    addEventListeners: function() {
        App.components.btnConvert.addEventListener("click", App.onConvertClicked);
        App.components.btnClear.addEventListener("click", App.onClearClicked);
        App.components.btnCopy.addEventListener("click", App.onCopyClicked);
        App.components.btnHelp.addEventListener("click", App.onHelpClicked);
        App.components.btnReaderView.addEventListener("click", App.onReaderViewClicked);

        App.components.btnHelpClose.forEach(item => {
            item.addEventListener("click", App.onHelpCloseClicked)
        });
        App.components.btnReaderViewClose.forEach(item => {
            item.addEventListener("click", App.onReaderViewCloseClicked)
        });
    },

    convertRecipe: function(recipe, multiplier) {
        return fetch(
            App.routes.convert,
            {
                headers: {'Content-Type': 'application/json'},
                method: "POST",
                body: JSON.stringify({ "data": recipe, "multiplier": multiplier })
            }
        )
        .then( response => response.json() )
        .then( function(response) {
                App.components.txtOutputRecipe.value = response["data"];
        });
    },

    appendInstructions: function(instructions) {
        App.components.txtOutputRecipe.value = App.components.txtOutputRecipe.value.concat(
            "\n\n", instructions
        );
    },

    onConvertClicked: function() {
        if (App.components.txtInputRecipe.value.includes("http")) {
            App.components.btnConvert.disabled = true;
            App.components.btnClear.disabled = true;

            // Get ingredients from URL, then convert
            fetch(
                App.routes.ingredientFromUrl,
                {
                    headers: {'Content-Type': 'application/json'},
                    method: "POST",
                    body: JSON.stringify({ "url": App.components.txtInputRecipe.value })
                }
            )
            .then( response => response.json() )
            .then(function (data) {
                App.components.txtInputRecipe.value = data["ingredients"] + "\n\n\n" + data["instructions"];

                App.convertRecipe(
                    data["ingredients"], App.components.txtInputMultiplier.value
                ).then(function() {
                    App.appendInstructions(data["instructions"])
                })
            }).catch(function () {
                alert("Parsing error: Website not supported for " + App.components.txtInputRecipe.value + "\n\nPlease manually copy the recipe into the input box.")
            }).then(function () {
                App.components.btnConvert.disabled = false;
                App.components.btnClear.disabled = false;
            })
        }
        else {
            var split_str = App.components.txtInputRecipe.value.split("\n\n\n")

            var ingredients = split_str[0]
            var instructions = split_str[1]

            console.debug(ingredients)
            console.debug(instructions)

            // Ingredients entered manually
            App.convertRecipe(
                ingredients, App.components.txtInputMultiplier.value
            )
            .then(function() {
                // Do this double replacement for formatting in case the final output has too many newlines
                // Happens when instructions already have two newlines in between them
                App.appendInstructions(instructions.replace(/\n/g, "\n\n").replace(/\n\s*\n/g, '\n\n'))
            })
        }
    },

    onClearClicked: function() {
        App.components.txtInputRecipe.value = "";
        App.components.txtInputRecipe.focus();
    },

    onCopyClicked: function() {
        copyToClipboard(App.components.txtOutputRecipe.value);

        // Change button text for user feedback
        const originalText = App.components.btnCopy.innerHTML;
        App.components.btnCopy.innerHTML = "Copied!";
        setTimeout(function() {
            App.components.btnCopy.innerHTML = originalText;
        }, 2000)
    },

    onHelpClicked: function() {
        App.components.modalHelp.classList.add("active");
    },

    onHelpCloseClicked: function() {
        App.components.modalHelp.classList.remove("active");
    },

    onReaderViewClicked: function() {
        App.components.txtReaderView.innerHTML = App.components.txtOutputRecipe.value;
        App.components.modalReaderView.classList.add("active")
    },

    onReaderViewCloseClicked: function() {
        App.components.modalReaderView.classList.remove("active")
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
