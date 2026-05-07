import streamlit as st
import yfinance as yf

def classify_stock(info):
    # Basic classification logic
    revenue_growth = info.get('revenueGrowth', 0) or 0
    pe_ratio = info.get('trailingPE', 100) or 100
    ps_ratio = info.get('priceToSalesTrailing12Months', 10) or 10
    
    # Criteria for Growth (Cathie Wood Style)
    if revenue_growth > 0.15 or ps_ratio > 8:
        return "Growth (Cathie Wood Style)"
    else:
        return "Value Investor"

def get_pros_cons(ticker, style, info):
    if "Growth" in style:
        pros = [
            f"High Revenue Growth ({info.get('revenueGrowth', 0)*100:.1f}%)",
            "Market leader in emerging technologies",
            "Significant investment in R&D",
            "High potential for industry disruption",
            "Strong institutional momentum"
        ]
        cons = [
            f"Premium valuation - High P/S ratio ({info.get('priceToSalesTrailing12Months', 'N/A')})",
            "Extreme price volatility",
            "High sensitivity to interest rate hikes",
            "High cash burn or lack of current profitability",
            "Increasing competition from Big Tech"
        ]
    else:
        pros = [
            f"Attractive P/E ratio ({info.get('trailingPE', 'N/A')})",
            "Stable and positive free cash flow",
            "Strong balance sheet with low debt-to-equity",
            "Consistent dividends or share buybacks",
            "High intrinsic value relative to market price"
        ]
        cons = [
            "Relatively slow top-line growth",
            "Risk of falling into a 'Value Trap'",
            "Exposure to traditional economic cycles",
            "Less attractive to momentum-driven investors",
            "Risk of technological obsolescence"
        ]
    return pros, cons

# UI Setup
st.set_page_config(page_title="Stock Classifier", layout="wide")
st.title("📈 Stock Classifier: Growth vs Value")

tickers_input = st.text_input("Enter Stock Tickers (separated by commas):", "TSLA, BRK-B, NVDA, JNJ")
tickers = [t.strip().upper() for t in tickers_input.split(",")]

if st.button("Analyze Stocks"):
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if not info or 'longName' not in info:
                st.warning(f"Could not find data for {ticker}")
                continue
                
            style = classify_stock(info)
            pros, cons = get_pros_cons(ticker, style, info)
            
            with st.expander(f"{ticker} - {info.get('longName', '')}"):
                st.subheader(f"Classification: **{style}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success("5 Reasons to BUY")
                    for p in pros: st.write(f"✅ {p}")
                with col2:
                    st.error("5 Reasons NOT to Buy")
                    for c in cons: st.write(f"❌ {c}")
                
                st.divider()
                st.write(f"**Key Metrics:** P/E: {info.get('trailingPE', 'N/A')} | P/S: {info.get('priceToSalesTrailing12Months', 'N/A')} | Growth: {info.get('revenueGrowth', 0)*100:.1f}%")
        except Exception as e:
            st.error(f"Error analyzing {ticker}: {e}")
