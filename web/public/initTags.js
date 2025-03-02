const getItemsTags = () => {
    const filters = {
        type: [],
        collection: [],
        category: [],
        quality: [],
        misk: [],
        graffiti_color: [],
        weapon: [],
        exterior: [],
        sticker_collection: [],
        sticker_type: [],
        tournament: [],
        team: [],
        professional_player: [],
    };

    const updateFilter = (filterArray, value) => {
        if (!value) return;
        const existing = filterArray.find((item) => item.name === value);
        if (existing) {
            existing.count += 1;
        } else {
            filterArray.push({ name: value, count: 1 });
        }
    };

    Array.from(initialItems).forEach((el) => {
        const attributes = el.querySelector("img");

        const type = attributes.getAttribute("data-type");
        const category = attributes.getAttribute("data-category");
        const quality = attributes.getAttribute("data-quality");
        const exterior = attributes.getAttribute("data-wear");

        const itemName = attributes
            .getAttribute("alt")
            .split("|")[0]
            .replace(category, "")
            .trim();

        updateFilter(filters.type, type);
        updateFilter(filters.category, category);
        updateFilter(filters.quality, quality);
        updateFilter(filters.exterior, exterior);

        if (
            type !== "sticker" &&
            type !== "agent" &&
            type !== "container" &&
            type !== "graffiti"
        ) {
            updateFilter(filters.weapon, itemName);
        }

        if (type === "agent" && itemName) {
            updateFilter(filters.professional_player, itemName);
        }
    });

    Object.keys(filters).forEach((key) => {
        const category = document.createElement("div");
        category.classList.add("econ_tag_filter_category");
        category.innerHTML += `<div class="econ_tag_filter_category_label">${capitalizeWords(
            key
        )}</div>`;

        const hiddenTags = document.createElement("div");
        hiddenTags.classList.add("econ_tag_filter_collapsable_tags");
        hiddenTags.style.display = "none";

        const items = filters[key];

        let addedShowMore = false;
        let showMoreButton = null;

        if (items && items.length > 0) {
            items.forEach((item, index) => {
                const colors = {
                    quality: {
                        extraordinary: "rgb(235, 75, 75)",
                        convert: "rgb(235, 75, 75)",
                        classified: "rgb(211, 44, 230)",
                        base_grade: "rgb(176, 195, 217)",
                        consumer_grade: "rgb(176, 195, 217)",
                        high_grade: "rgb(75, 105, 255)",
                        "mil-spec_grade": "rgb(75, 105, 255)",
                        industrial_grade: "rgb(94, 152, 217)",
                        industrial_grade: "rgb(94, 152, 217)",
                        remarkable: "rgb(136, 71, 255)",
                        restricted: "rgb(136, 71, 255)",
                    },
                    category: {
                        "StatTrak™": "rgb(207, 106, 50)",
                        "★_StatTrak™": "rgb(134, 80, 172)",
                        "★": "rgb(134, 80, 172)",
                    },
                };

                const defaultColor = "#969696";

                const currentColor =
                    colors?.[key]?.[item.name.replaceAll(" ", "_")] ||
                    defaultColor;

                const additionalStyles = `style="color: ${currentColor}"`;
                const itemHtml = `
        <div class="econ_tag_filter_container">
            <input class="econ_tag_filter_checkbox" type="checkbox"
            onchange="filtersChange(this, event, '${key}', '${item.name}')"
                name="tag_filter_them_730_2_Type_CSGO_${item.name}"
                id="tag_filter_them_730_2_Type_CSGO_${item.name}"
                tag_name="CSGO_Type_WeaponCase">
            <label class="econ_tag_filter_label"
                for="tag_filter_them_730_2_Type_CSGO_${
                    item.name
                }" ${additionalStyles}>
                ${capitalizeWords(item.name.split("_").join(" ").trim())}
                <span class="econ_tag_count" style="color: ${defaultColor}">(${
                    item.count
                })</span>
            </label>
        </div>`;

                if (index < 5) {
                    category.innerHTML += itemHtml;
                } else {
                    hiddenTags.innerHTML += itemHtml;
                    if (!addedShowMore) {
                        addedShowMore = true;
                        showMoreButton = document.createElement("div");
                        showMoreButton.classList.add(
                            "econ_tag_filter_collapsable_tags_showlink",
                            "whiteLink"
                        );
                        showMoreButton.innerText = "+ Show more";
                        showMoreButton.onclick = () => {
                            hiddenTags.style.display = "block";
                            showMoreButton.style.display = "none";
                        };
                    }
                }
            });

            tags.appendChild(category);

            if (addedShowMore) {
                category.appendChild(showMoreButton);
                category.appendChild(hiddenTags);
            }
        }
    });
};

getItemsTags();
