from controller.main_controller import MainController
from view.main_view import MainView


def main_ui():
    """ Main function. """
    # Create instances of the model and the controller
    view = MainView()
    model = None
    MainController(model=model, view=view)


if __name__ == '__main__':
    main_ui()
