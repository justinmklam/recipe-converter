var btnConvert = $("#btn-convert")
var btnClear = $("#btn-clear")
var btnCopy = $("#btn-copy")
var btnHelp = $("#btn-help")
var btnHelpClose = $(".btn-help-close")
var btnReaderView = $("#btn-reader-view")
var btnReaderViewClose = $(".btn-reader-view-close")
var txtInputRecipe = $("#input-recipe")
var txtInputMultiplier = $("#input-multiplier")
var txtReaderView = $("#reader-view-content")
var txtOutputRecipe = $("#output-recipe")
var modalReaderView = $("#reader-view")
var modalHelp = $("#modal-help")

window.addEventListener("load", function () {
    btnConvert.on("click", onConvertClicked);
    btnClear.on("click", onClearClicked);
    btnCopy.on("click", onCopyClicked);
    btnHelp.on("click", onHelpClicked);
    btnHelpClose.on("click", onHelpCloseClicked);
    btnReaderView.on("click", onReaderViewClicked);
    btnReaderViewClose.on("click", onReaderViewCloseClicked);
});

function convertRecipe(recipe, multiplier) {
    return $.post(
        "convert",
        { "data": recipe, "multiplier": multiplier },
        function (data) {
            txtOutputRecipe.val(data);
        }
    );
}

function onConvertClicked() {
    if (txtInputRecipe.val().includes("http")) {
        btnConvert.prop("disabled", true);
        btnClear.prop("disabled", true);

        // Get ingredients from URL, then convert
        $.post(
            "ingredients_from_url",
            { "url": txtInputRecipe.val() },
            function (data) {
                txtInputRecipe.val(data["ingredients"])
                convertRecipe(data["ingredients"], txtInputMultiplier.val())
                    .done(function () {
                        // Append instructions below recipe
                        console.log(data["instructions"])
                        txtOutputRecipe.val(function () {
                            return this.value + "\n\n" + data["instructions"]
                        })
                    })
            }
        )
            .fail(function () {
                alert("Parsing error: Website not supported for " + txtInputRecipe.val() + "\n\nPlease manually copy the recipe into the input box.")
            })
            .always(function () {
                btnConvert.prop("disabled", false);
                btnClear.prop("disabled", false);
            })
    }
    else {
        var split_str = txtInputRecipe.val().split("\n\n\n")

        var ingredients = split_str[0]
        var instructions = split_str[1]

        console.debug(ingredients)
        console.debug(instructions)

        // Ingredients entered,
        convertRecipe(ingredients, txtInputMultiplier.val())
            .done(function () {
                // Append instructions below recipe
                txtOutputRecipe.val(function () {
                    // Add additional line break for readability
                    return this.value + "\n\n" + instructions.replace(/\n/g, "\n\n")
                })
            })
    }
}

function onClearClicked() {
    txtInputRecipe.val("");
    txtInputRecipe.focus();
}

function onCopyClicked() {
    copyToClipboard(txtOutputRecipe.val());
    new Toast({ message: 'Output recipe copied to clipboard!', type: 'success' });
}

function onHelpClicked() {
    modalHelp.addClass("active");
}

function onHelpCloseClicked() {
    modalHelp.removeClass("active");
}

function onReaderViewClicked() {
    txtReaderView.text(txtOutputRecipe.val());
    console.log(txtOutputRecipe.val())
    modalReaderView.addClass("active")
}

function onReaderViewCloseClicked() {
    modalReaderView.removeClass("active")
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
