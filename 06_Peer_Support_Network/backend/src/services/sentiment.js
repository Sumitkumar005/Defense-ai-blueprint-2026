/**
 * Sentiment analysis service using NLP
 * PLACEHOLDER: In production, would use BERT model
 */

class SentimentAnalyzer {
  async analyzeCheckIn(text) {
    /**
     * Analyze sentiment of check-in text
     * Returns sentiment score and concerning keywords
     */
    
    // PLACEHOLDER: Would use BERT for sentiment analysis
    const concerningKeywords = [
      'hopeless', 'suicide', 'end it', 'no point', 'worthless'
    ];
    
    const lowerText = text.toLowerCase();
    const hasConcerningContent = concerningKeywords.some(keyword => 
      lowerText.includes(keyword)
    );
    
    // Simple sentiment (would be BERT in production)
    const positiveWords = ['good', 'great', 'fine', 'okay', 'happy'];
    const negativeWords = ['bad', 'terrible', 'awful', 'sad', 'depressed'];
    
    let sentiment = 0.5; // Neutral
    const positiveCount = positiveWords.filter(w => lowerText.includes(w)).length;
    const negativeCount = negativeWords.filter(w => lowerText.includes(w)).length;
    
    if (positiveCount > negativeCount) {
      sentiment = 0.7;
    } else if (negativeCount > positiveCount) {
      sentiment = 0.3;
    }
    
    return {
      sentimentScore: sentiment,
      hasConcerningContent,
      requiresEscalation: hasConcerningContent || sentiment < 0.3
    };
  }
}

module.exports = new SentimentAnalyzer();

