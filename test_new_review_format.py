#!/usr/bin/env python3
"""
Test New Review Format
Shows the improved structured analysis format
"""

import asyncio
import sys
sys.path.append('.')

from fresh_scanner import analyze_with_perplexity, simple_crypto_analysis

async def test_new_format():
    """Test the new structured review format"""
    
    print("🧪 TESTING NEW STRUCTURED REVIEW FORMAT")
    print("=" * 60)
    
    # Example test message 
    test_message = """
    We're excited to announce Vanilla Finance's OTC round. 
    24-month lockup, $100M FDV, targeting $500M-$800M post-TGE.
    DeFi protocol with leverage features, legal counsel and escrow involved.
    Looking for strategic investors with OTC discount vs public launch.
    """
    
    print("📝 Test Message:")
    print(f'"{test_message.strip()}"')
    print("\n" + "=" * 60)
    
    try:
        # Test Perplexity analysis with new format
        print("\n📊 PERPLEXITY ANALYSIS (New Structured Format):")
        print("-" * 50)
        
        perplexity_result = await analyze_with_perplexity(test_message)
        if perplexity_result:
            project_name = perplexity_result.get('project_name', 'Unknown')
            score = perplexity_result.get('confidence_score', 0)
            analysis = perplexity_result.get('detailed_analysis', 'No analysis')
            
            print(f"🏷️  Project: {project_name}")
            print(f"📈 Score: {score}%")
            print(f"\n📋 Structured Analysis:")
            print(analysis)
        else:
            print("❌ No Perplexity analysis returned")
        
        print("\n" + "=" * 60)
        
        # Test fallback analysis with new format
        print("\n🔄 FALLBACK ANALYSIS (New Structured Format):")
        print("-" * 50)
        
        fallback_result = simple_crypto_analysis(test_message)
        if fallback_result:
            project_name = fallback_result.get('project_name', 'Unknown')
            score = fallback_result.get('confidence_score', 0)
            analysis = fallback_result.get('detailed_analysis', 'No analysis')
            
            print(f"🏷️  Project: {project_name}")
            print(f"📈 Score: {score}%")
            print(f"\n📋 Structured Analysis:")
            print(analysis)
        else:
            print("❌ No fallback analysis generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ NEW REVIEW FORMAT FEATURES:")
    print("🔹 ✅ Pros: Lists positive aspects and strengths")
    print("🔹 ⚠️ Risks/Red Flags: Highlights concerns and weaknesses") 
    print("🔹 🔎 What Are These Guys Doing: Explains business model/strategy")
    print("🔹 Structured and easy to scan in Google Sheets")
    print("🔹 Consistent format for both Perplexity and fallback analysis")

def show_expected_format():
    """Show the expected format example"""
    
    print("\n📋 EXPECTED GOOGLE SHEETS REVIEW FORMAT:")
    print("=" * 60)
    
    expected_review = """Score: 75% | ✅ Pros:
• Early access to tokens at potentially better prices
• OTC discount potential vs. public launch  
• Regulatory fit: legal counsel and escrow involved
• Good traction if project is strong (DeFi + leverage = hot narrative)

⚠️ Risks / Red Flags:
• Long lockup (24 months) → Low liquidity
• FDV $100M might be overpriced if no product or revenue yet
• No anti-dilution or reporting rights
• Unclear who the OTC lead is — trust is essential
• Still subject to crypto market volatility and regulatory changes

🔎 What Are These Guys Doing?
They are organizing a private investment round for Vanilla Finance using tokens that already exist (or will exist) but not through a public launch. Their aim is to raise capital quickly, give early liquidity to existing shareholders, and attract strategic investors through a discounted OTC deal. This is typical of pre-launch DeFi protocols trying to bootstrap liquidity."""
    
    print(expected_review)
    print("\n✅ This format will appear in Column E (Review) of your Google Sheet!")

async def main():
    await test_new_format()
    show_expected_format()

if __name__ == "__main__":
    asyncio.run(main()) 