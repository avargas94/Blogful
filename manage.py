import os
from flask_script import Manager

from blog import app

from blog.database import session, Entry

manager = Manager(app)


@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    print(port)

@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ornare egestas arcu id bibendum. 
    Fusce tempus felis ac interdum pretium. Maecenas aliquam ipsum sed tortor eleifend, vitae tincidunt sem lobortis. 
    Phasellus ac varius nisl, nec dignissim purus. Maecenas vel egestas massa, id lacinia dolor. 
    Morbi a lorem ac turpis fringilla eleifend. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in 
    posuere purus, in elementum lorem. In ut ante sit amet sem ultricies consectetur. 
    
    """
    for i in range(25):
        entry = Entry(
            title="Test Entry #{}".format(i),
            content=content
        )
        session.add(entry)
    session.commit()


if __name__ == "__main__":
    manager.run()
