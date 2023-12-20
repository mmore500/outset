document.addEventListener("DOMContentLoaded", function() {
    // Function to create and append toggle button
    function addToggleButton(div) {
        var button = document.createElement("button");
        button.innerHTML = "Show Code »";

        // Styling the button
        button.style.backgroundColor = "#F5F5F5"; // Light grey background
        button.style.color = "#333333"; // Dark text color
        button.style.border = "1px solid #DDD"; // Light grey border
        button.style.padding = "2px 5px"; // Padding inside the button
        button.style.marginTop = "5px"; // Margin at the top
        button.style.cursor = "pointer"; // Cursor to indicate clickable
        button.style.borderRadius = "3px"; // Rounded corners
        button.style.fontSize = "0.9em"; // Font size
        button.style.width = "100%"; // Full width of the button
        button.style.maxWidth = "100px"; // Max width of the button
        button.style.transition = "max-width 0.5s ease, background-color 1s ease"; // Animation for width and background-color

        // Initial hide style for div
        div.style.opacity = '0';
        div.style.maxHeight = '0px';
        div.style.overflow = 'hidden';
        div.style.transition = 'opacity 0.2s ease, max-height 0.6s ease'; // Animation for opacity and max-height

        button.onclick = function() {
            if (div.style.maxHeight === '0px') {
                div.style.opacity = '1';
                div.style.maxHeight = '500px'; // Adjust as needed to fit the content
                button.innerHTML = "»» Hide Code ««";
                // button.style.width = "100%";
                button.style.maxWidth = "100%";
            } else {
                div.style.opacity = '0';
                div.style.maxHeight = '0px';
                button.innerHTML = "Show Code »";
                button.style.maxWidth = "100px";
            }
        };

        div.parentNode.insertBefore(document.createElement("hr"), div);
        div.parentNode.insertBefore(button, div);
    }

    // Select and hide code and output divs
    var codeDivs = document.querySelectorAll('.nbinput.docutils.container');
    codeDivs.forEach(function(div) {
        // div.style.display = 'none';
        addToggleButton(div);
    });

    var outputDivs = document.querySelectorAll('.prompt, .stderr.docutils.container');
    outputDivs.forEach(function(div) {
        div.style.display = 'none';
    });
});
