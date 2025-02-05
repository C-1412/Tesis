def show_user(user):
    return user.groups.filter(name__in=['Administrador', 'Moderador']).exists()     
