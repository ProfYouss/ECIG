from nicegui import ui, app
import base64
import os
from datetime import datetime
import shutil

# Setup static files directory
os.makedirs('static', exist_ok=True)
app.add_static_files('/static', 'static')

# Runtime storage using dictionaries
posts = []  # List to store all posts
users = {}  # Dictionary to store user credentials


css = '''
            .container {
              width: 100%;
              height: 100%;
              background: radial-gradient(
                    circle farthest-side at 0% 50%,
                    #282828 23.5%,
                    rgba(255, 170, 0, 0) 0
                  )
                  21px 30px,
                radial-gradient(
                    circle farthest-side at 0% 50%,
                    #2c3539 24%,
                    rgba(240, 166, 17, 0) 0
                  )
                  19px 30px,
                linear-gradient(
                    #282828 14%,
                    rgba(240, 166, 17, 0) 0,
                    rgba(240, 166, 17, 0) 85%,
                    #282828 0
                  )
                  0 0,
                linear-gradient(
                    150deg,
                    #282828 24%,
                    #2c3539 0,
                    #2c3539 26%,
                    rgba(240, 166, 17, 0) 0,
                    rgba(240, 166, 17, 0) 74%,
                    #2c3539 0,
                    #2c3539 76%,
                    #282828 0
                  )
                  0 0,
                linear-gradient(
                    30deg,
                    #282828 24%,
                    #2c3539 0,
                    #2c3539 26%,
                    rgba(240, 166, 17, 0) 0,
                    rgba(240, 166, 17, 0) 74%,
                    #2c3539 0,
                    #2c3539 76%,
                    #282828 0
                  )
                  0 0,
                linear-gradient(90deg, #2c3539 2%, #282828 0, #282828 98%, #2c3539 0%) 0 0
                  #282828;
              background-size: 40px 60px;
            }
'''
like_button_css = '''
 
                #heart {
                  display: none;
                }

                .like-button {
                  position: relative;
                  cursor: pointer;
                  display: flex;
                  height: 48px;
                  width: 136px;
                  border-radius: 16px;
                  border: none;
                  background-color: #1d1d1d;
                  overflow: hidden;
                  box-shadow:
                    inset -2px -2px 5px rgba(255, 255, 255, 0.2),
                    inset 2px 2px 5px rgba(0, 0, 0, 0.1),
                    4px 4px 10px rgba(0, 0, 0, 0.4),
                    -2px -2px 8px rgba(255, 255, 255, 0.1);
                }

                .like {
                  width: 70%;
                  height: 100%;
                  display: flex;
                  cursor: pointer;
                  align-items: center;
                  justify-content: space-evenly;
                }

                .like-icon {
                  fill: #505050;
                  height: 28px;
                  width: 28px;
                }

                .like-text {
                  color: #fcfcfc;
                  font-size: 16px;
                  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                }

                .like-count {
                  position: absolute;
                  right: 0;
                  width: 30%;
                  height: 100%;
                  display: flex;
                  justify-content: center;
                  align-items: center;
                  color: #717070;
                  font-size: 16px;
                  border-left: 2px solid #4e4e4e;
                  transition: all 0.5s ease-out;
                }

                .like-count.two {
                  transform: translateY(40px);
                }

                .on:checked ~ .like .like-icon {
                  fill: #fc4e4e;
                  animation: enlarge 0.2s ease-out 1;
                  transition: all 0.2s ease-out;
                }

                .on:checked ~ .like-count.two {
                  transform: translateX(0);
                  color: #fcfcfc;
                }

                .on:checked ~ .like-count.one {
                  transform: translateY(-40px);
                }

                @keyframes enlarge {
                  0% {
                    transform: scale(0.5);
                  }
                  100% {
                    transform: scale(1.2);
                  }
                }
            '''



@ui.page('/signup')
def signup():
    global css, profilepic
    profilepic = 'static/profile.jpg'
    ui.add_css(css)
    ui.query('body').classes('container')
    if app.storage.user.get('logged_in'):
        return ui.navigate.to('/home')
    async def handle_upload(e):
        global profilepic
        profilepic = e.name
        data64 = base64.b64encode(e.content.read())
        with open(f'static/{profilepic}', 'wb') as f:
            f.write(base64.b64decode(data64))
        
    with ui.card().classes('w-96 mx-auto mt-8'):
        ui.label('Sign Up').classes('text-2xl font-bold mb-4')
        ui.upload(
            label='Profile Picture',
            on_upload=handle_upload,
            auto_upload=True
        ).classes('w-full')
        username = ui.input('Username').classes('w-full mb-2')
        password = ui.input('Password', password=True).classes('w-full mb-2')
        confirm_password = ui.input('Confirm Password', password=True).classes('w-full mb-2')

        def handle_signup():
            global profilepic
            print(profilepic)
            if not username.value or not password.value or not confirm_password.value:
                ui.notify('Please fill all fields', color='red')
                return
                
            if username.value in users:
                ui.notify('Username already exists', color='red')
                return
                
            if password.value != confirm_password.value:
                ui.notify('Passwords do not match', color='red')
                return
            
                
            # Create new user
            users[username.value] = {
                'password': password.value,
                'joined_date': datetime.now().strftime('%Y-%m-%d'),
            }
            app.storage.user["profile_pic"] = profilepic
            ui.notify('Account created successfully!', color='green')
            ui.navigate.to('/')
        
        ui.button('Sign Up', on_click=handle_signup).classes('w-full mt-4')
        ui.link('Already have an account? Login', '/').classes('mt-4 block text-center')

@ui.page('/')
def login():
    global css
    ui.add_css(css)
    ui.query('body').classes('container')
    if app.storage.user.get('logged_in'):
        return ui.navigate.to('/home')
    
    with ui.card().classes('w-96 mx-auto mt-8'):
        ui.label('Login').classes('text-2xl font-bold mb-4')
        username = ui.input('Username').classes('w-full mb-2')
        password = ui.input('Password', password=True).classes('w-full mb-2')
        
        def handle_login():
            if username.value not in users:
                ui.notify('User not found', color='red')
                return
                
            if users[username.value]['password'] != password.value:
                ui.notify('Invalid password', color='red')
                return
                
            app.storage.user['username'] = username.value
            app.storage.user['logged_in'] = True
            app.storage.user['joined_date'] = users[username.value]['joined_date']
            ui.navigate.to('/home')
        
        ui.button('Login', on_click=handle_login).classes('w-full mt-4')
        ui.link('Need an account? Sign Up', '/signup').classes('mt-4 block text-center')
        
@ui.page('/home')
def home():
    global css
    ui.add_css(css)
    ui.add_css(like_button_css)
    ui.query('body').classes('container')
    if not app.storage.user.get('logged_in'):
        return ui.navigate.to('/')
    
    # Navigation bar
    with ui.row().classes('w-1/2 self-center justify-between p-4 bg-blue-100'):
        ui.label(f'Welcome {app.storage.user.get("username")}!')
        with ui.row():
            ui.link('Home', '/home').classes('mr-4')
            ui.link('Profile', '/profile').classes('mr-4')
            
            def logout():
                app.storage.user.clear()
                ui.navigate.to('/')
            
            ui.button('Logout', on_click=logout)
    
    # Create post section
    with ui.card().classes('w-1/2 self-center bg-black'):
        ui.label('Create Post').classes('text-xl text-white font-bold')
        caption = ui.input('Caption').classes('w-full bg-white')
        
        async def handle_upload(e):
            
            
            filename = e.name
            
            data64 = base64.b64encode(e.content.read())
            with open(f'static/{filename}', 'wb') as f:
                f.write(base64.b64decode(data64))
            filepath = f'static/{filename}'
            
            
            # Create new post
            new_post = {
                'id': len(posts),
                'username': app.storage.user['username'],
                'image_path': f'/static/{filename}',
                'caption': caption.value,
                'likes': set(),
                'comments': [],
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            posts.insert(0, new_post)  # Add to beginning of posts
            
            # Clear input and refresh
            caption.value = ''
            ui.notify('Post created!', color='green')
            ui.navigate.to('/home')
            
        
        ui.upload(
            label='Upload Content',
            on_upload=handle_upload,
            auto_upload=True
        ).classes('w-full')
    
    # Posts display
    posts_container = ui.card().classes('w-1/2 self-center')
    
    
        
        # ... (previous code remains the same)

    def refresh_posts():
        posts_container.clear()
        with posts_container:
            if len(posts) == 0:
                ui.image('static/empty.png').classes('w-full h-full object-contain')
            for post in posts:
                with ui.card().classes('w-full mx-auto mb-4'):
                    with ui.row().classes('justify-between items-center'):
                        ui.label(f"Posted by: {post['username']}").classes('font-bold')
                        ui.label(post['created_at']).classes('text-sm text-gray-500')
                    if post['image_path'].endswith('mp4'):
                        ui.video(post['image_path']).classes('w-full')
                    else:
                        ui.image(post['image_path']).classes('w-full')
                    ui.label(post['caption'])
                    
                    # Like button
                    def toggle_like(post=post):  # Capture the specific post
                        username = app.storage.user['username']
                        if username in post['likes']:
                            post['likes'].remove(username)
                        else:
                            post['likes'].add(username)
                        refresh_posts()
                        
                    
                    ui.html(f'''
                    <div class="like-button">
                      <input class="on" id="heart" type="checkbox" />
                      <label class="like" for="heart">
                        <svg
                          class="like-icon"
                          fill-rule="nonzero"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z"
                          ></path>
                        </svg>
                        <span class="like-text">Likes</span>
                      </label>
                      <span class="like-count one">{len(post['likes'])}</span>
                      <span class="like-count two">{len(post['likes']) - 1 if app.storage.user['username'] in post['likes'] else len(post['likes']) + 1}</span>
                    </div>
                    ''').on('click', toggle_like)  # Directly call toggle_like
                    
                    # Comments
                    ui.label('Comments:').classes('font-bold mt-2')
                    for comment in post['comments']:
                        ui.label(f"{comment['username']}: {comment['text']}")
                    
                    # Add comment
                    with ui.row().classes('w-full'):
                        comment_input = ui.input('Add comment...').classes('flex-grow')
                        
                        def add_comment(post=post):
                            if comment_input.value.strip():
                                post['comments'].append({
                                    'username': app.storage.user['username'],
                                    'text': comment_input.value,
                                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                                })
                                comment_input.value = ''
                                refresh_posts()
                        
                        ui.button('Post', on_click=add_comment)

    # ... (rest of the code remains the same)
    
    refresh_posts()

@ui.page('/profile')
def profile():
    global css
    ui.add_css(css)
    ui.query('body').classes('container')
    if not app.storage.user.get('logged_in'):
        return ui.navigate.to('/')
    
    # Navigation bar (same as home)
    with ui.row().classes('w-1/2 self-center justify-between p-4 bg-blue-100'):
        ui.label(f'Profile: {app.storage.user.get("username")}')
        with ui.row():
            ui.link('Home', '/home').classes('mr-4')
            ui.link('Profile', '/profile').classes('mr-4')
            
            def logout():
                app.storage.user.clear()
                ui.navigate.to('/')
            
            ui.button('Logout', on_click=logout)
    
    # Profile info
     # Add the card CSS
    card_css = '''
    .card {
      overflow: visible;
      width: 620px;
      height: 254px;
    }

    .content {
      width: 100%;
      height: 100%;
      transform-style: preserve-3d;
      transition: transform 300ms;
      box-shadow: 0px 0px 10px 1px #000000ee;
      border-radius: 5px;
    }

    .front, .back {
      background-color: #151515;
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 5px;
      overflow: hidden;
    }

    .back {
      width: 100%;
      height: 100%;
      justify-content: center;
      display: flex;
      align-items: center;
      align-self: center;
      overflow: hidden;
    }

    .back::before {
      position: absolute;
      content: ' ';
      display: block;
      width: 160px;
      height: 160%;
      background: linear-gradient(90deg, transparent, #ff9966, #ff9966, #ff9966, #ff9966, transparent);
      animation: rotation_481 5000ms infinite linear;
    }

    .back-content {
      position: absolute;
      width: 99%;
      height: 99%;
      background-color: #151515;
      border-radius: 5px;
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 30px;
    }

    .card:hover .content {
      transform: rotateY(180deg);
    }

    @keyframes rotation_481 {
      0% {
        transform: rotateZ(0deg);
      }

      100% {
        transform: rotateZ(360deg);
      }
    }

    .front {
      transform: rotateY(180deg);
      color: white;
    }

    .front .front-content {
      position: absolute;
      width: 100%;
      height: 100%;
      padding: 10px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .front-content .badge {
      background-color: #00000055;
      padding: 2px 10px;
      border-radius: 10px;
      backdrop-filter: blur(2px);
      width: fit-content;
    }

    .description {
      box-shadow: 0px 0px 10px 5px #00000088;
      width: 100%;
      padding: 10px;
      background-color: #00000099;
      backdrop-filter: blur(5px);
      border-radius: 5px;
    }

    .title {
      font-size: 11px;
      max-width: 100%;
      display: flex;
      justify-content: space-between;
    }

    .title p {
      width: 50%;
    }

    .card-footer {
      color: #ffffff88;
      margin-top: 5px;
      font-size: 8px;
    }

    .front .img {
      position: absolute;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
    }

    .circle {
      width: 90px;
      height: 90px;
      border-radius: 50%;
      background-color: #ffbb66;
      position: relative;
      filter: blur(15px);
      animation: floating 2600ms infinite linear;
    }

    #bottom {
      background-color: #ff8866;
      left: 50px;
      top: 0px;
      width: 150px;
      height: 150px;
      animation-delay: -800ms;
    }

    #right {
      background-color: #ff2233;
      left: 160px;
      top: -80px;
      width: 30px;
      height: 30px;
      animation-delay: -1800ms;
    }

    @keyframes floating {
      0% {
        transform: translateY(0px);
      }

      50% {
        transform: translateY(10px);
      }

      100% {
        transform: translateY(0px);
      }
    }
    '''
    ui.add_css(card_css)
    ui.add_css('''
    .avatar {
      vertical-align: middle;
      width: 100px;
      height: 100px;
      border-radius: 50%;
      object-contain;
    }''')
    
    # Profile card
    with ui.column().classes('flex justify-center items-center self-center').style('margin-right:0px'):
        ui.html('''
        <div class="card">
          <div class="content">
            <div class="back">
              <div class="back-content">
                <img src='static/{profile_pic}' alt="Profile Picture" class="avatar">
                <strong>{username}</strong>
              </div>
            </div>
            <div class="front">
              <div class="img">
                <div class="circle"></div>
                <div class="circle" id="right"></div>
                <div class="circle" id="bottom"></div>
              </div>
              <div class="front-content">
                <small class="badge">User</small>
                <div class="description">
                  <div class="title">
                    <p class="title">
                      <strong>{username}</strong>
                    </p>
                  </div>
                  <p class="card-footer">
                    Joined: {joined_date}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        '''.format(
            username=app.storage.user.get("username"),
            joined_date=app.storage.user.get("joined_date"),
            profile_pic=app.storage.user.get("profile_pic")
        ))
    
    # Display user's posts
    with ui.card().classes('w-1/2 self-center'):
        user_posts = [post for post in posts if post['username'] == app.storage.user['username']]
        ui.label(f"Your Posts ({len(user_posts)})").classes('text-xl font-bold mt-4')
        if len(user_posts) == 0:
                ui.image('static/profile.jpg').classes('w-full h-full object-contain')
        for post in user_posts:
            with ui.card().classes('w-full mx-auto mb-4'):
                if post['image_path'].endswith('mp4'):
                        ui.video(post['image_path']).classes('w-full')
                else:
                        ui.image(post['image_path']).classes('w-full')
                ui.label(post['caption'])
                ui.label(f"Posted on: {post['created_at']}")
                ui.label(f"Likes: {len(post['likes'])}")
                ui.label(f"Comments: {len(post['comments'])}")

ui.run(storage_secret='FGHJK fghgjhkj')
