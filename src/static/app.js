const themeToggle = document.getElementById("themeToggle");
const savedTheme = localStorage.getItem("fraud-monitor-theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");
}

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-theme");

        const selectedTheme =
            document.body.classList.contains("dark-theme")
                ? "dark"
                : "light";

        localStorage.setItem(
            "fraud-monitor-theme",
            selectedTheme
        );
    });
}

document.querySelectorAll("[data-width]").forEach((element) => {
    const rawWidth = Number(element.dataset.width || 0);
    const safeWidth = Math.min(100, Math.max(0, rawWidth));

    window.requestAnimationFrame(() => {
        element.style.width = `${safeWidth}%`;
    });
});

const transactionSearch =
    document.getElementById("transactionSearch");

const riskFilter =
    document.getElementById("riskFilter");

const transactionRows = Array.from(
    document.querySelectorAll(
        "#transactionTable tbody tr[data-risk]"
    )
);

function filterTransactions() {
    const searchValue =
        transactionSearch?.value.toLowerCase().trim() || "";

    const selectedRisk =
        riskFilter?.value || "ALL";

    transactionRows.forEach((row) => {
        const matchesText = row.textContent
            .toLowerCase()
            .includes(searchValue);

        const matchesRisk =
            selectedRisk === "ALL" ||
            row.dataset.risk === selectedRisk;

        row.style.display =
            matchesText && matchesRisk ? "" : "none";
    });
}

if (transactionSearch) {
    transactionSearch.addEventListener(
        "input",
        filterTransactions
    );
}

if (riskFilter) {
    riskFilter.addEventListener(
        "change",
        filterTransactions
    );
}

document.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
        document
            .querySelectorAll(".nav-link")
            .forEach((item) => {
                item.classList.remove("active");
            });

        link.classList.add("active");
    });
});