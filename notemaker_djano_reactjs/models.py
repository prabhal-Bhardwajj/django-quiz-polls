from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.contrib.auth.models import User

class NoteCategory(models.TextChoices):
    PERSONAL = 'Personal', _('Personal')
    GRATITUDE = 'Gratitude', _('Gratitude')
    INSIGHT = 'Insight', _('Insight')
    REFLECTION = 'Reflection', _('Reflection')
    MINDBYTE = 'Mindbyte', _('Mindbyte')
    MATHEMATICS = 'Mathematics', _('Mathematics')
    ASTROLOGY = 'Astrology', _('Astrology')
    MACHINE_LEARNING = 'Machine_Learning', _('Machine_Learning')
    PROGRAMMING = 'Programming', _('Programming')
    LITERATURE = 'Literature', _('Literature')
    POETRY = 'Poetry', _('Poetry')
    CINEMA = 'Cinema', _('Cinema')
    PHILOSOPHY = 'Philosophy', _('Philosophy')
    RELIGION = 'Religion', _('Religion')
    INFORMATION = 'Information', _('Information')
    THOUGHTS = 'Thoughts', _('Thoughts')
    TASKS = 'Tasks', _('Tasks')
    NOTES = 'Notes', _('Notes')
    NEWS = 'News', _('News')
    RANDOM = 'Random', _('Random')
    PHYSICS = 'Physics', _('Physics')
    WORK = 'Work', _('Work')
    STUDY = 'Study', _('Study')
    FINANCE = 'Finance', _('Finance')
    TRAVEL = 'Travel', _('Travel')
    RECIPES = 'Recipes', _('Recipes')
    PROJECTS = 'Projects', _('Projects')
    IDEAS = 'Ideas', _('Ideas')
    HEALTH = 'Health', _('Health')
    REMINDERS = 'Reminders', _('Reminders')
    POLITY = 'Polity', _('Polity')
    DJANGO = 'Django', _('Django')
    ECONOMY = 'Economy', _('Economy')
    CULTURE = 'Culture', _('Culture')
    FRONT_END_PROGRAMMING = 'F_E_Programming', _('F_E_Programming')
    CPPLANGUAGE = 'CPP Language', _('CPP Language')
    GEOGRAPHY = 'Geography', _('Geography')
    JAVA = 'Java', _('Java')
    PYTHON = 'Python', _('Python')
    HISTORY = 'History', _('History')
    ART = 'Art', _('Art')
    MUSIC = 'Music', _('Music')
    SCIENCE_TECH = 'Science & Tech', _('Science & Tech')
    ASTRONOMY = 'Astronomy', _('Astronomy')
    BIOLOGY = 'Biology', _('Biology')
    STATISTICS = 'Statistics', _('Statistics')
    ENVIRONMENT = 'Environment', _('Environment')
    CURRENT_AFFAIRS = 'Current Affairs', _('Current Affairs')
    UNMARKED = 'Unmarked', _('Unmarked')
class Notes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    
    category = models.CharField(
        max_length=30,
        choices=NoteCategory.choices,
        default=NoteCategory.UNMARKED
    )
    
    

    def is_protected(self):
        return bool(self.password)

    def save(self, *args, **kwargs):
        # Hash the password before saving if it exists
        if self.password:
            self.password = make_password(self.password)

        # Optionally, validate category (though already handled by `choices`)
        if self.category not in [choice[0] for choice in NoteCategory.choices]:
            raise ValueError(f"Invalid category: {self.category}")
        
        # Call the parent class's save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
class CornellNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cornell_notes')
    title = models.CharField(max_length=200)
    show_title = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    show_dates = models.BooleanField(default=True)
    
    
    cues_questions = models.TextField(
        _('Cues/Questions'),
        blank=True,
        help_text="Key questions or main ideas"
    )
    main_notes = models.TextField(
        _('Main Notes'),
        help_text="Detailed notes content"
    )
    summary = models.TextField(
        _('Summary'),
        blank=True,
        help_text="Key takeaways and conclusions"
    )
    
    category = models.CharField(
        max_length=30,
        choices=NoteCategory.choices,
        default=NoteCategory.UNMARKED
    )
    
    # Security Purpose
    is_protected = models.BooleanField(default=False)
    password = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
        help_text="Optional password protection"
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Cornell Notes'

    def save(self, *args, **kwargs):
        # Handle password protection
        if self.is_protected and self.password:
            self.password = make_password(self.password)
        elif not self.is_protected:
            self.password = None
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    def is_locked(self):
        return self.is_protected and bool(self.password)