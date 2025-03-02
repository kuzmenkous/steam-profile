let currentPage = 1;
let pageChanges = false;

const blockButtons = () => {
    const prevBtn = document.getElementById("pagebtn_previous");
    const nextBtn = document.getElementById("pagebtn_next");
    const currentPageElement = document.getElementById("pagecontrol_cur");
    const maxPagesElement = document.getElementById("pagecontrol_max");

    currentPageElement.innerText = currentPage;
    maxPagesElement.innerText = pages.length || 1;

    if (currentPage <= 1) {
        prevBtn.classList.add("disabled");
    } else {
        prevBtn.classList.remove("disabled");
    }

    if (currentPage >= pages.length) {
        nextBtn.classList.add("disabled");
    } else {
        nextBtn.classList.remove("disabled");
    }
};

const transitionTime = 300;

const InventoryNextPage = () => {
    if (pageChanges) return;

    if (currentPage < (pages.length || 1)) {
        currentPage++;

        blockButtons();

        pages.forEach((page, index) => {
            const targetIndex = currentPage - 1 || 0;
            const pageParent = page.parentNode;
            pageParent.style.overflow = "hidden";
            setTimeout(() => {
                pageParent.style.width = "832px";
            }, 10);
            pageChanges = true;
            page.style.transition = `${transitionTime}ms linear`;

            if (index === targetIndex) {
                page.style.display = "block";
                page.style.transform = "unset";

                setTimeout(() => {
                    page.style.transform = "translateX(-100%)";
                }, 10);

                setTimeout(() => {
                    page.style.transition = "none";
                    page.style.transform = "unset";
                }, transitionTime);
            } else if (index === targetIndex - 1) {
                page.style.transform = "translateX(-100%)";

                setTimeout(() => {
                    page.style.display = "none";
                }, transitionTime);
            } else {
                page.style.display = "none";
            }
        });

        setTimeout(() => {
            pages.forEach((page) => {
                const pageParent = page.parentNode;
                pageParent.style.width = "416px";
                pageParent.style.overflow = "visible";
            });
            pageChanges = false;
        }, transitionTime);
    }
};

const InventoryPreviousPage = () => {
    if (pageChanges) return;

    if (currentPage > 1) {
        currentPage--;

        blockButtons();

        pages.forEach((page, index) => {
            const targetIndex = currentPage - 1 || 0;
            const pageParent = page.parentNode;
            pageParent.style.overflow = "hidden";
            setTimeout(() => {
                pageParent.style.width = "832px";
            }, 10);
            pageChanges = true;
            page.style.transition = `${transitionTime}ms linear`;

            if (index === targetIndex) {
                page.style.display = "block";
                page.style.transform = "translateX(-100%)";

                setTimeout(() => {
                    page.style.transform = "unset";
                }, 10);

                setTimeout(() => {
                    page.style.transition = "none";
                    page.style.transform = "unset";
                }, transitionTime);
            } else if (index === targetIndex + 1) {
                page.style.transform = "unset";

                setTimeout(() => {
                    page.style.transform = "translateX(100%)";
                }, 10);

                setTimeout(() => {
                    page.style.display = "none";
                }, transitionTime);
            } else {
                page.style.display = "none";
            }
        });

        setTimeout(() => {
            pages.forEach((page) => {
                const pageParent = page.parentNode;
                pageParent.style.width = "416px";
                pageParent.style.overflow = "visible";
                pageChanges = false;
            });
        }, transitionTime);
    }
};
