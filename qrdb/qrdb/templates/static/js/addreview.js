window.addEventListener("load", function () {
    var $pageTitle = document.getElementById("page-title");
    var $$pages = document.querySelectorAll("section");
    var maxPage = $$pages.length - 1;
    var page = 0;

    var $previousButton = document.getElementById("previous");
    var $nextButton = document.getElementById("next");

    function updatePage(delta) {
        page = Math.max(Math.min(page + delta, maxPage), 0);

        $pageTitle.innerText = $$pages[page].dataset.title;
        $previousButton.disabled = page === 0;
        $nextButton.innerText = page === maxPage ? "Submit" : "Next →";

        for(var i = 0; i <= maxPage; i++) {
            $$pages[i].style.display = i === page ? "block" : "none";
        }

        document.body.scrollTop = 0; // Safari
        document.documentElement.scrollTop = 0; // Chrome, Firefox, IE
    }
    updatePage(0);

    $previousButton.addEventListener("click", function (e) {
        e.preventDefault();
        updatePage(-1);
    });
    $nextButton.addEventListener("click", function (e) {
        if(page === maxPage) return; // just submit form
        e.preventDefault();
        updatePage(1);
    });


    var $$fileInputs = document.querySelectorAll("input[type=file]");
    $$fileInputs.forEach(function ($fileInput) {
        var $fileDisplay = document.getElementById($fileInput.dataset.fileDisplay);
        if (!$fileDisplay) return;

        function updateFileDisplay() {
            $fileDisplay.innerHTML = "";
            Array.prototype.slice.call($fileInput.files).forEach(function (file) {
                var src = URL.createObjectURL(file);
                if (file.type.startsWith("image/")) {
                    var $img = document.createElement("img");
                    $img.src = src;
                    $fileDisplay.appendChild($img);
                } else if (file.type.startsWith("video/")) {
                    var $video = document.createElement("video");
                    $video.controls = true;
                    var $videoSource = document.createElement("source");
                    $videoSource.src = src;
                    $videoSource.type = file.type;
                    $video.appendChild($videoSource);
                    $fileDisplay.appendChild($video);
                }
            });
        }

        $fileInput.addEventListener("change", updateFileDisplay);
        updateFileDisplay();
    });
});