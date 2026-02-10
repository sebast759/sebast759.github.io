document.addEventListener('DOMContentLoaded', function () {
  const baseUrl = 'https://tame-cap.s3.us-east-1.amazonaws.com/public/TG_PROD/Dashboard/Plot_Universe_Graphs/';

  // Helper to switch active class
  function setActive(buttons, activeBtn) {
    buttons.forEach(b => b.classList.remove('active'));
    activeBtn.classList.add('active');
  }

  // Crypto rainbow chart buttons
  const cryptoBtns = Array.from(document.querySelectorAll('.crypto-tab-btn'));
  const cryptoImg = document.getElementById('crypto-chart');
    // Replace "MTD" and "Previous M" labels with current/previous month in short-month + 2-digit year format (e.g. Feb26)
    if (cryptoBtns.length) {
        const now = new Date();
        const monthAbbr = new Intl.DateTimeFormat('en', { month: 'short' }).format(now);
        const yy = now.getFullYear().toString().slice(-2);
        const mtdLabel = `${monthAbbr}${yy}`;
        const prev = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        const prevAbbr = new Intl.DateTimeFormat('en', { month: 'short' }).format(prev);
        const prevLabel = `${prevAbbr}${prev.getFullYear().toString().slice(-2)}`;
        const mtdBtn = cryptoBtns.find(b => b.dataset.period === 'mtd');
        const prevBtn = cryptoBtns.find(b => b.dataset.period === 'previous');
        if (mtdBtn) mtdBtn.textContent = mtdLabel;
        if (prevBtn) prevBtn.textContent = prevLabel;
    }



  // Price action buttons
  const priceBtns = Array.from(document.querySelectorAll('.price_action-tab-btn'));
  const priceImg = document.getElementById('price-action-chart');
  if (priceBtns.length && priceImg) {
    priceBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        setActive(priceBtns, btn);
        const period = btn.dataset.period.toUpperCase();
        // pattern: price_action_<SYMBOL>_2024 (keep existing pattern)
        priceImg.src = baseUrl + `price_action_${period}_2024`;
      });
    });
  }
});
// Tab switching
function showTab(tabName) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));
    
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Crypto period switching

// Crypto tabs
document.querySelectorAll('.crypto-tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const period = this.dataset.period;
        showCryptoPeriod(period, this);
    });
});

function showCryptoPeriod(period, btn) {
    const urls = {
        'today': 'today_performance_rainbow',
        'yesterday': 'yesterday_performance_rainbow',
        'mtd': 'mtd_performance_rainbow',
        'previous': 'prev_m_performance_rainbow',
        'ytd': 'ytd_performance_rainbow',
        '2025': 'year_2025_performance_rainbow',
        '2024': 'year_2024_performance_rainbow'
    };
    document.getElementById('crypto-chart').src = 
        'https://tame-cap.s3.us-east-1.amazonaws.com/public/TG_PROD/Dashboard/Plot_Universe_Graphs/' + urls[period];
    
    document.querySelectorAll('.crypto-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

// Bond maturity switching
// Bond maturity switching (radio buttons)
document.querySelectorAll('input[name="maturity"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const maturity = this.value;
        document.getElementById('bond-chart').src = 
            `bond_yield_curves/yield_curves_${maturity}.html`;
    });
});
// Ranked yields maturity switching
document.querySelectorAll('input[name="ranked-maturity"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const maturity = this.value;
        document.getElementById('ranked-chart').src = 
            `bond_yield_curves/yields_${maturity}_ranked.html`;
    });
});

// Rolldown spread switching
document.querySelectorAll('input[name="rolldown-spread"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const spread = this.value;
        document.getElementById('rolldown-chart').src = 
            `bond_yield_curves/spread_${spread}.html`;
    });
});

// Historical chart region switching
document.querySelectorAll('input[name="history-region"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const region = this.value;
        let filename;

        if (region === 'eu-spread') {
            filename = 'graphs/bond_yield_curves/history_EU_spread_vs_germany.html';
        } else if (region === 'g5') {
            filename = 'graphs/bond_yield_curves/history_g5_10y.html';
        } else if (region === 'eu') {
            filename = 'graphs/bond_yield_curves/history_eu_10y.html';
        } else if (region === 'all') {
            filename = 'graphs/bond_yield_curves/history_all_10y.html';
        } else {
            filename = 'graphs/bond_yield_curves/history_g5_10y.html';
        }

        document.getElementById('history-chart').src = filename;
    });
});

// Historical chart country switching (individual countries)
document.querySelectorAll('input[name="history-country"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const country = this.value;
        const filename = `graphs/bond_yield_curves/history_${country}_10y.html`;
        document.getElementById('history-chart').src = filename;
    });
});

// Price action button switching (BTC/ETH)
document.querySelectorAll('.price_action-tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const asset = this.dataset.period.toUpperCase();
        document.getElementById('price-action-chart').src =
            `https://tame-cap.s3.us-east-1.amazonaws.com/public/TG_PROD/Dashboard/Plot_Universe_Graphs/price_action_${asset}_2024`;

        document.querySelectorAll('.price_action-tab-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
    });
});

// Treemap button switching (YTD/2025/2024)
document.querySelectorAll('.treemap-tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const period = this.dataset.period;
        let url;

        if (period === 'ytd') {
            url = 'https://tame-cap.s3.amazonaws.com/public/TG_PROD/Dashboard/Plot_Universe_Graphs/treemap_ytd';
        } else if (period === '2024') {
            url = 'https://tame-cap.s3.amazonaws.com/public/TG_PROD/Dashboard/Plot_Universe_Graphs/treemap_year_2024';
        } else if (period === '2025') {
            url = 'https://tame-cap.s3.amazonaws.com/public/TG_PROD/Dashboard/Plot_Universe_Graphs/treemap_year_2025';
        }

        document.getElementById('treemap-chart').src = url;

        document.querySelectorAll('.treemap-tab-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
    });
});