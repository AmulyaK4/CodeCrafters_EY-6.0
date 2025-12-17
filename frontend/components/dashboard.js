export function renderDashboard(container) {
  container.innerHTML = "";
}

export function updateDashboard(container, data) {
  const cards = [
    { title: "Trials", value: `${data.trials?.length || 0} active` },
    { title: "Patents", value: `${data.patents?.length || 0} relevant` },
    {
      title: "Market",
      value: data.market?.market_size_usd
        ? `$${(data.market.market_size_usd / 1e9).toFixed(1)}B / CAGR ${data.market.cagr || 0}%`
        : "n/a",
    },
    { title: "Papers", value: `${data.papers?.length || 0} recent` },
    { title: "Score", value: data.summary?.score ?? "n/a" },
  ];
  container.innerHTML = cards
    .map(
      (c) => `<div class="p-3 border rounded mb-2 bg-gray-50">
      <div class="text-sm text-gray-500">${c.title}</div>
      <div class="text-lg font-semibold">${c.value}</div>
    </div>`
    )
    .join("");
}

