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
        'ytd': 'ytd_performance_rainbow'
    };
    
    document.getElementById('crypto-chart').src = 
        'https://tame-cap.s3.us-east-1.amazonaws.com/TG_PROD/Dashboard/Plot_Universe_Graphs/' + urls[period];
    
    document.querySelectorAll('.crypto-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}