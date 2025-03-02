const filters = {};

const filtersChange = (element, event, filterType, value) => {
    if (filterType === "search") {
        filters[filterType] = value.toLowerCase().trim();
    } else {
        if (!filters[filterType]) {
            filters[filterType] = [];
        }

        if (element.checked) {
            filters[filterType].push(value);
        } else {
            filters[filterType] = filters[filterType].filter(
                (filter) => filter !== value
            );
        }

        if (filters[filterType].length === 0) {
            delete filters[filterType];
        }
    }

    applyFilters();
};

const applyFilters = () => {
    const inventoryElement = document.getElementById(
        "inventory_76561198244722344_730_2"
    );
    const maxItemsPerPage = 16;

    const resetPages = () => {
        currentPages.forEach((page) => page.remove());
        let currentPageItems = [];
        let currentPageIndex = 0;

        const filteredItems = Array.from(initialItems).filter(
            (item) => item.style.display !== "none"
        );

        filteredItems.forEach((item, index) => {
            if (item.parentNode?.classList.contains("trade_slot")) {
                const innerItem = item.querySelector('div[id*="item730"]');
                const newSlotId = innerItem?.id + "_slot";
                const slot = document.createElement("div");
                slot.classList.add("itemHolder");
                slot.id = newSlotId;
                currentPageItems.push(slot);
            } else {
                currentPageItems.push(item);
            }

            if (
                currentPageItems.length === maxItemsPerPage ||
                index === filteredItems.length - 1
            ) {
                const newPage = document.createElement("div");
                newPage.classList.add("inventory_page");

                if (currentPageIndex > 0) newPage.style.display = "none";

                currentPageItems.forEach((itemElement) => {
                    newPage.appendChild(itemElement);
                });

                const remainingSpace =
                    maxItemsPerPage - currentPageItems.length;
                for (let i = 0; i < remainingSpace; i++) {
                    const disabledSlot = document.createElement("div");
                    disabledSlot.classList.add("itemHolder", "disabled");
                    newPage.appendChild(disabledSlot);
                }

                inventoryElement.appendChild(newPage);
                currentPageItems = [];
                currentPageIndex++;
            }
        });

        const newCurrentPages =
            inventoryElement.querySelectorAll(".inventory_page");
        newCurrentPages.forEach(
            (page, index) => (page.style.display = index < 1 ? "block" : "none")
        );
        pages = newCurrentPages;
    };

    initialItems.forEach((item) => {
        if (item.parentNode?.classList.contains("trade_slot")) return;
        const img = item.querySelector("img");
        let shouldShow = true;

        for (const [filterType, values] of Object.entries(filters)) {
            if (filterType === "search") {
                const searchQuery = values.toLowerCase();
                const itemName = img.getAttribute("alt").toLowerCase();

                if (!itemName.includes(searchQuery)) {
                    shouldShow = false;
                    break;
                }
            } else {
                const currentValues = values.map((value) =>
                    value.toLowerCase()
                );

                if (filterType !== "weapon") {
                    const itemAttribute = img
                        .getAttribute(`data-${filterType}`)
                        .toLowerCase();
                    if (
                        currentValues.length > 0 &&
                        !currentValues.includes(itemAttribute)
                    ) {
                        shouldShow = false;
                        break;
                    }
                } else {
                    const itemQuality = img
                        .getAttribute("data-quality")
                        .toLowerCase();
                    const itemName = img
                        .getAttribute("alt")
                        .split("|")[0]
                        .replace(itemQuality, "")
                        .trim()
                        .toLowerCase();

                    if (
                        currentValues.length > 0 &&
                        !currentValues.includes(itemName)
                    ) {
                        shouldShow = false;
                        break;
                    }
                }
            }
        }

        item.style.display = shouldShow ? "block" : "none";
    });

    const currentPages = inventoryElement.querySelectorAll(".inventory_page");
    if (JSON.stringify(filters) !== "{}") {
        const availableItems = Array.from(initialItems).filter(
            (element) =>
                element.style.display !== "none" &&
                !element.parentNode.classList.contains("trade_slot")
        );

        currentPages.forEach((page) => page.remove());

        let currentPageItems = [];
        let currentPageIndex = 0;

        availableItems.forEach((item, index) => {
            if (item.parentNode?.classList.contains("trade_slot")) return;
            currentPageItems.push(item);

            if (
                currentPageItems.length === maxItemsPerPage ||
                index === availableItems.length - 1
            ) {
                const newPage = document.createElement("div");
                newPage.classList.add("inventory_page");

                if (currentPageIndex > 0) newPage.style.display = "none";

                currentPageItems.forEach((itemElement) => {
                    newPage.appendChild(itemElement);
                });

                const remainingSpace =
                    maxItemsPerPage - currentPageItems.length;

                for (let i = 0; i < remainingSpace; i++) {
                    const disabledSlot = document.createElement("div");
                    disabledSlot.classList.add("itemHolder", "disabled");
                    newPage.appendChild(disabledSlot);
                }

                inventoryElement.appendChild(newPage);
                currentPageItems = [];
                currentPageIndex++;
            }
        });

        const newCurrentPages =
            inventoryElement.querySelectorAll(".inventory_page");
        pages = newCurrentPages;
    } else {
        resetPages();
    }

    currentPage = 1;
    blockButtons();
};

const searchInput = document.getElementById("filter_control");

searchInput.addEventListener("input", (e) => {
    filtersChange(null, e, "search", e.target.value);
});
