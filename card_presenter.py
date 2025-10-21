"""
Card Presenter - Handles Anki card interactions
"""

from typing import Optional
from anki.cards import Card
from anki.collection import Collection
from aqt import mw


class CardPresenter:
    """Manages Anki card presentation and answering"""
    
    def __init__(self, col: Collection, config: dict):
        self.col = col
        self.config = config
        
    def get_next_card(self) -> Optional[Card]:
        """Get the next card due for review"""
        # Use Anki's scheduler to get the next card
        card = self.col.sched.getCard()
        return card
        
    def get_card_question(self, card: Card) -> str:
        """Extract the question from a card"""
        if not card:
            return ""
            
        # Get the question side of the card
        question = card.question()
        
        # Strip HTML tags for cleaner text presentation
        question = self._strip_html(question)
        
        return question
        
    def get_card_answer(self, card: Card) -> str:
        """Extract the answer from a card"""
        if not card:
            return ""
            
        # Get the answer side of the card
        answer = card.answer()
        
        # Strip HTML tags
        answer = self._strip_html(answer)
        
        return answer
        
    def answer_card(self, card: Card, ease: int):
        """Answer the card with the given ease"""
        if not card:
            return
            
        # Ease values: 1=Again, 2=Hard, 3=Good, 4=Easy
        # Use Anki's scheduler to answer the card
        self.col.sched.answerCard(card, ease)
        
        # Save changes to database
        self.col.autosave()
        
    def _strip_html(self, html: str) -> str:
        """Strip HTML tags from text"""
        import re
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Replace common HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&amp;', '&')
        text = text.replace('&quot;', '"')
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
        
    def get_cards_due_count(self) -> int:
        """Get the number of cards due for review"""
        counts = self.col.sched.counts()
        return counts[0]  # New cards + review cards
