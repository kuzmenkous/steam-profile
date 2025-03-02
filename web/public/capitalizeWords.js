function capitalizeWords(string) {
    return string
        .split(" ")
        .map((word) => {
            if (word.includes("-")) {
                return word
                    .split("-")
                    .map(
                        (subWord) =>
                            subWord.charAt(0).toUpperCase() + subWord.slice(1)
                    )
                    .join("-");
            }
            return word.charAt(0).toUpperCase() + word.slice(1);
        })
        .join(" ");
}
