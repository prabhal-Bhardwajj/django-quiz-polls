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