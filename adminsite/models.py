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
    processeur_choices =(("i3","i3"),("i5","i5"),("i7","i7"),("i9","i9"),("ryzen3","ryzen3"),("ryzen5","ryzen5"),("ryzen7","ryzen7"))
    processeur = models.CharField(max_length=20, choices=processeur_choices,null=True)
    memoire_choices = (("64Go","64Go"),("32Go","32Go"),("16Go","16Go"),("8Go","8Go"))
    memoire = models.CharField(max_length=20, choices=memoire_choices, null=True)
    stockage_choices =(("1To","1To"),("512Go","512Go"),("256Go","256Go"), ("128Go","128Go"), ("64Go","64Go"), ("32Go","32Go"))
    stockage = models.CharField(max_length=20, choices=stockage_choices, null=True)

    def __str__(self):
        return f" {self.nom} {self.type} avec un processeur {self.processeur} et une memoire de {self.memoire} avec un stockage de {self.stockage}"

    def dico(self):
        return {"nom": self.nom, "type": self.type,"processeur": self.processeur,"memoire": self.memoire,"stockage": self.stockage}


class Utilisateurs(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return f" {self.nom} {self.prenom}, {self.email}"

    def dico(self):
        return {"nom": self.nom, "prenom": self.prenom,"email": self.email}



class Applications(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='images/', null=True)
    utilisateurs = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, null=True, related_name="utilisateurs")
    serveur = models.ForeignKey(Serveurs, on_delete=models.CASCADE, null=True, related_name="serveur")

    def __str__(self):
        return f"{self.nom}, sur le {self.serveur} de l'utilisateur {self.utilisateurs}"

    def dico(self):
        return {"nom": self.nom, "logo": self.logo.file,"serveur": self.serveur,"utilisateurs": self.utilisateurs}


class Services(models.Model):
    nom = models.CharField(max_length=30)
    date = models.DateField()
    stockage_use = models.CharField(max_length=8)
    memoire_vive = models.CharField(max_length=8)
    serveur_lancement = models.ForeignKey(Serveurs, on_delete=models.CASCADE, null=True, related_name="serveur_lancement")
    def __str__(self):
        return f" {self.nom},le {self.date} utilisant {self.stockage_use} de stockage , nécessitant {self.memoire_vive} de mémoire , sur le serveur : {self.serveur_lancement}"

    def dico(self):
        return {"nom": self.nom, "date": self.date,"memoire_use": self.stockage_use,"stockage_use": self.memoire_vive,"serveur_lancement": self.serveur_lancement}

