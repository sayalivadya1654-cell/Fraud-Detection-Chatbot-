def chatbot_reply(user_query, inputs, category):
    try:
        user_query = user_query.lower()

        # Specific Fraud Detection Logic
        if "check fraud" in user_query or "fraud" in user_query or "suspicious" in user_query:
            if category == "upi":
                amount = float(inputs.get("amount", 0))
                if amount > 10000:
                    return "🚨 This UPI transaction looks suspicious because of high amount."
                elif not inputs.get("upi_id") or not inputs.get("sender") or not inputs.get("receiver"):
                    return "❗ UPI ID, sender, or receiver information is missing. Can't verify properly."
                return "✅ This UPI transaction seems safe."

            elif category == "credit card":
                cvv = str(inputs.get("cvv", ""))
                card_number = str(inputs.get("card_number", ""))
                if len(cvv) != 3:
                    return "🚨 CVV should be exactly 3 digits. This looks suspicious."
                if not card_number.isdigit() or len(card_number) < 12:
                    return "🚨 Card number seems invalid. It might be a fraudulent attempt."
                return "✅ This Credit Card transaction appears normal."

            elif category == "url":
                url = inputs.get("url", "").lower()
                suspicious_keywords = ["free", "click", "win", ".xyz", ".ss", "vega", "earn", "login", "bank", "confirm"]
                risky_found = [kw for kw in suspicious_keywords if kw in url]
                if risky_found:
                    return f"🚨 This URL appears suspicious. It contains risky words like: {', '.join(risky_found)}"
                return "✅ This URL seems safe and clean."

        # FAQs (General queries)
        elif "cvv" in user_query:
            return "🔐 CVV means Card Verification Value — a 3-digit number on your card. Keep it confidential to prevent fraud."

        elif "upi" in user_query:
            return "💡 UPI fraud often happens when someone asks for money using fake links or payment requests. Never share OTPs or click unverified links."

        elif "url" in user_query:
            return "🌐 Fake URLs often use misspellings, unknown extensions (.xyz, .ss), or demand urgent actions like 'click now'. Be careful."

        elif "is fraud" in user_query or "is it fraud" in user_query:
            return "🧐 I need full details of your transaction to check if it's fraud. Please fill in all required fields."

        # General category-based fallback if no specific user_query
        elif category == "upi":
            return "UPI transaction seems safe."

        elif category == "credit card":
            return "Credit Card transaction looks suspicious!"

        elif category == "url":
            return "URL is potentially fraudulent!"

        elif category == "faq":
            return "You can ask me about fraud detection, UPI safety, or scam prevention."

        else:
            return "🤖 I can help detect UPI, credit card, or suspicious URLs. Ask about CVV, UPI fraud, or fake links."

    except Exception as e:
        return f"❌ Error processing input: {e}"
