from django.db import models

class Types(models.Model):
    test_choices = (("Apache","Apache"),("SQL","SQL"),("DNS","DNS"),("Proxy","Proxy"),("Imap","Imap"))
    type = models.CharField(max_length=20, choices=test_choices, null=True)
    description = models.TextField(null = True, blank = True)

    def __str__(self):
        return f"{self.type}"

    def dico(self):
        return {"type": self.type, "description": self.description}


class Serveurs(models.Model):
    nom = models.CharField(max_length=100)
    type = models.ForeignKey(Types, on_delete=models.CASCADE, null=True, related_name="Type")
    processeur = models.IntegerField(max_length=20,null=True)
    memoire_choices = (("64Go","64Go"),("32Go","32Go"),("16Go","16Go"),("8Go","8Go"))
    memoire = models.CharField(max_length=20, choices=memoire_choices, null=True)
    stockage_choices =(("1To","1To"),("512Go","512Go"),("256Go","256Go"), ("128Go","128Go"), ("64Go","64Go"), ("32Go","32Go"))
    stockage = models.CharField(max_length=20, choices=stockage_choices, null=True)
    stockage_initial = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f" {self.nom} ( {self.type} )"

    def dico(self):
        return {"nom": self.nom, "type": self.type,"processeur": self.processeur,"memoire": self.memoire,"stockage": self.stockage,"stockage_initial": self.stockage_initial}


class Utilisateurs(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return f" {self.nom} {self.prenom}"

    def dico(self):
        return {"nom": self.nom, "prenom": self.prenom,"email": self.email}



class Applications(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='images/', null=True, blank=True, default="images/applications_default.jpg")
    utilisateurs = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, null=True, related_name="utilisateurs")
    serveur = models.ForeignKey(Serveurs, on_delete=models.CASCADE, null=True, related_name="serveur")
    def __str__(self):
        return f"{self.nom}, sur le {self.serveur} de l'utilisateur {self.utilisateurs}"

    def dico(self):
        return {"nom": self.nom, "logo": self.logo.file,"serveur": self.serveur,"utilisateurs": self.utilisateurs}


class Services(models.Model):
    nom = models.CharField(max_length=30)
    date = models.DateField()
    stockage_use = models.CharField(max_length=18,null=True)
    memoire_vive = models.CharField(max_length=18,null=True)
    serveur_lancement = models.ForeignKey(Serveurs, on_delete=models.CASCADE, null=True, related_name="serveur_lancement")
    def __str__(self):
        return f" {self.nom},le {self.date} utilisant {self.stockage_use} de stockage , nécessitant {self.memoire_vive} de mémoire , sur le serveur : {self.serveur_lancement}"

    def dico(self):
        return {"nom": self.nom, "date": self.date,"stockage_use": self.stockage_use,"memoire_vive": self.memoire_vive,"serveur_lancement": self.serveur_lancement}

