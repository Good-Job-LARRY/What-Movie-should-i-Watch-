from inspect import Parameter
from multiprocessing import Value
from textwrap import wrap
import requests  
import tkinter as tk
from datetime import datetime
import locale 
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os 
import json
import urllib.request
import random
import io
import webbrowser
from urllib.parse import quote
import math
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


TMDB_API_KEY = "89bd81b58ee3a4c71d9ffc79ca2b4795"  

TMDB_GENRES = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35, 
    "Documentary": 99, "Drama": 18, "Fantasy": 14, "Horror": 27, 
    "Sci-Fi": 878, "Thriller": 53049
}

global genre

genre = ["Action", "Adventure", "Animation", "Comedy", "Documentary", "Drama", "Fantasy","Horror","Sci-Fi","Thriller"]
genre_index = 0
def FinalMovie():
    rootQuiz.destroy()
    if Review == True:
        sort = "vote_average.desc"
    else:
        sort = "popularity.desc"
        
   
    genre_id = TMDB_GENRES.get(genre_name, "")
    paramaters = {
        "with_genres": f"{genre_id},{interests}" if interests else str(genre_id),
        "sort_by": sort,
        "vote_count.gte": 100 
    }
    if StartYear:
        paramaters["primary_release_date.gte"] = f"{StartYear}-01-01"
    if EndYear:
        paramaters["primary_release_date.lte"] = f"{EndYear}-12-31"

    recommendFile = getMovies(paramaters)
    data = recommendFile.get("titles", [])
    matchingMovies = [
        movie for movie in data
        if startLength < movie.get("runtimeSeconds", 0) < length
    ]
    if not matchingMovies:
        rootFinal = tk.Tk()
        rootFinal.geometry("500x200")
        rootFinal.config(bg="tomato1")
        rootFinal.resizable(False, False)
        tk.Label(rootFinal, text="No movies match your criteria.",
                 font=('Haettenschweiler', 24), bg="tomato1", fg="snow", wraplength=450).pack(expand=True, padx=20, pady=20)
        rootFinal.mainloop()
        return

    with open("RecommendedMovie.json", "w") as file3:
        json.dump(matchingMovies, file3, indent=3)

    with open("RecommendedMovie.json", "r") as file3:
        recommended_list = json.load(file3)
    Final = random.choice(recommended_list)

    rootFinal = tk.Tk()
    rootFinal.geometry("970x910")
    rootFinal.title("Your Final Movie")
    rootFinal.config(bg="tomato1")
    rootFinal.resizable(False, False)
    rootFinal._image_references = []

    movieTitle = Final.get("primaryTitle", "Unknown")
    moviePlot = Final.get("plot", "No plot available.")
    movieYear = Final.get("startYear", "")
    image_url = Final.get("primaryImage", {}).get("url", "")
    poster_size = (230, 350)

    tk.Label(rootFinal, text="Your recommended movie",
            font=('Haettenschweiler', 36), bg="snow", fg="grey1").pack(pady=20)


    try:
        if image_url:
            with urllib.request.urlopen(image_url, timeout=10) as u:
                img_data = u.read()
            pil_img = Image.open(io.BytesIO(img_data))
        else:
            pil_img = _PLACEHOLDER_IMAGE
    except Exception:
        pil_img = _PLACEHOLDER_IMAGE
    poster_img = pil_img.resize(poster_size, Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(poster_img)
    rootFinal._image_references.append(photo)
    poster_label = tk.Label(rootFinal, image=photo, bg="snow", borderwidth=5, relief="solid", highlightthickness=0)
    poster_label.pack(pady=(0, 10))

    title_text = movieTitle if not movieYear else f"{movieTitle} ({movieYear})"
    tk.Label(rootFinal, text=title_text, font=('Haettenschweiler', 28), bg="tomato1", fg="snow").pack(pady=(0, 10))

    plot_frame = tk.Frame(rootFinal, bg="snow", relief="solid", borderwidth=3, padx=15, pady=15)
    plot_frame.pack(pady=10, padx=80, fill="both", expand=True)
    tk.Label(plot_frame, text="Plot", font=('Haettenschweiler', 22), bg="snow", fg="grey1").pack(anchor="w")
    tk.Label(plot_frame, text=moviePlot, font=('MS Gothic', 16), bg="snow", fg="grey1", wraplength=750, justify="left").pack(anchor="w")

    def open_trailer():
        query = quote(f"{movieTitle} trailer")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    trailer_btn = tk.Button(rootFinal, text="Watch trailer", font=('Haettenschweiler', 24), bg="snow", fg="grey1", command=open_trailer)
    trailer_btn.pack(pady=20)

    rootFinal.mainloop()
def Quiz(position):
    
    #root.destroy()
    root3.destroy()
    global rootQuiz
    rootQuiz =tk.Tk()
    rootQuiz.geometry("970x910")
    rootQuiz.title = ("Movie Recommandations")
    rootQuiz.config(bg = "tomato1")
    rootQuiz.resizable(False,False)
    rootQuiz._image_references = [] 
    paramaters = {"Id": idArray[position]}
    
    
    request2 = requests.get(f"https://api.themoviedb.org/3/movie/{idArray[position]}?api_key={TMDB_API_KEY}")
    tmdb_movie = request2.json()
    

    YourFav = {
        "primaryTitle": tmdb_movie.get("title", "Unknown"),
        "interests": [{"name": g.get("name"), "id": g.get("id"), "isSubgenre": True} for g in tmdb_movie.get("genres", [])]
    }
    
    with open("YourFav.json","w") as file :
        json.dump(YourFav,file, indent = 3)
    MainTitle = tk.Label(rootQuiz, text = "Personality Quiz", font=('Haettenschweiler', 36), bg="snow", fg="grey1")
    MainTitle.place(x= 350, y= 50)
   
    containerFrame = tk.Frame(rootQuiz, bg="snow", relief="solid", borderwidth=5, width=400, height=700)
    containerFrame.place(x=290, y=160)
    containerFrame.pack_propagate(False)
    
   
    canvas = tk.Canvas(containerFrame, bg="snow", highlightthickness=0)
    scrollbar = tk.Scrollbar(containerFrame, orient="vertical", command=canvas.yview)
   
    scrollable_frame = tk.Frame(canvas, bg="snow", width=390, height=1600)
    
    def update_scroll_region(event=None):
        canvas.update_idletasks()
        bbox = canvas.bbox("all")
        if bbox:
            canvas.configure(scrollregion=bbox)
    
    scrollable_frame.bind("<Configure>", update_scroll_region)
    
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def on_canvas_configure(event):
       
        canvas_width = event.width
        if canvas_width > 1:
            canvas.itemconfig(canvas_window, width=canvas_width)
            scrollable_frame.config(width=canvas_width)
    
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.bind("<Configure>", on_canvas_configure)
    
   
    idFrame = scrollable_frame
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "images/crimb paper.jpg")
    imageBar_path = os.path.join(script_dir, "images/barcode.png")
    imageBar = Image.open(imageBar_path)
    imageBar = imageBar.convert("RGBA")
    imageBar = imageBar.resize((300, 90), Image.Resampling.LANCZOS)
    imageBar_photo = ImageTk.PhotoImage(imageBar)
    rootQuiz._image_references.append(imageBar_photo)
    imageBar_img = tk.Label(idFrame, image=imageBar_photo, borderwidth=0, highlightthickness=0)
    imageBar_img.place(x=0, y=1450)
    topPop = Image.open(image_path)
    topPop = topPop.convert("RGBA")

    topPop = topPop.resize((390, int(900 * 390 / 700)), Image.Resampling.LANCZOS)
    topPop_photo = ImageTk.PhotoImage(topPop)
    rootQuiz._image_references.append(topPop_photo) 
    topPop_img = tk.Label(idFrame, image = topPop_photo, borderwidth=0, highlightthickness=0)
    topPop_img.place(x = 0, y= 0)
    
    topPop2 = topPop.resize((390, int(900 * 390 / 700)), Image.Resampling.LANCZOS)
    topPop_photo2 = ImageTk.PhotoImage(topPop2)
    rootQuiz._image_references.append(topPop_photo2)  # Keep reference
    topPop_img2 = tk.Label(idFrame, image = topPop_photo2, borderwidth=0, highlightthickness=0)
    topPop_img2.place(x = 0, y= 390)
    image2_path = os.path.join(script_dir, "images/real image.png")
    topPop3 = topPop.resize((390, int(900 * 390 / 700)), Image.Resampling.LANCZOS)
    topPop_photo3 = ImageTk.PhotoImage(topPop3)
    rootQuiz._image_references.append(topPop_photo3)  # Keep reference
    topPop_img3 = tk.Label(idFrame, image = topPop_photo3, borderwidth=0, highlightthickness=0)
    topPop_img3.place(x = 0, y=850)
    topPop4 = topPop.resize((390, int(900 * 390 / 700)), Image.Resampling.LANCZOS)
    topPop_photo4 = ImageTk.PhotoImage(topPop4)
    rootQuiz._image_references.append(topPop_photo4)  # Keep reference
    topPop_img4 = tk.Label(idFrame, image = topPop_photo4, borderwidth=0, highlightthickness=0)
    topPop_img4.place(x = 0, y= 1300)
    logo = Image.open(image2_path)
    logo = logo.convert("RGBA")
    logo = logo.resize((120,120),Image.Resampling.LANCZOS)
    logoPhoto = ImageTk.PhotoImage(logo)
    rootQuiz._image_references.append(logoPhoto)  # Keep reference
    logoimg = tk.Label(idFrame, image = logoPhoto, borderwidth=0, highlightthickness=0) 
    logoimg.place(x = 150, y = 10)
    lblCinema = tk.Label(idFrame, text = "Movie ticket", font = ('Haettenschweiler', 16), bg="snow", fg="grey1")
    lblCinema.place(x= 160, y= 100)
    lblCinema.lift()
    today2 = datetime.now()
    today2 = today2.strftime("%Y-%m-%d")
    time = tk.Label(idFrame, text = today2,font=('MS Gothic', 20),  bg = "snow")
    time.place(x=200, y= 150)
    lblDate =  tk.Label(idFrame, text = "Date:",font=('MS Gothic', 20), bg = "snow")
    lblDate.place(x= 0, y =150)
    lblName = tk.Label(idFrame, text= "Name???:",font=('MS Gothic', 20),  bg = "snow")
    lblName.place(y = 200)
    edtName = tk.Entry(idFrame,font=('Haettenschweiler', 20), width = 20)
    edtName.place(x = 200, y = 200)
    lblAge = tk.Label(idFrame, text = "Age???:", font = ('MS Gothic', 20), bg="snow", fg="grey1")
    lblAge.place(y= 250)
    sedtAge= tk.Spinbox(idFrame, font=('Haettenschweiler', 20), from_=6, to=100, width = 10)
    sedtAge.place(x= 200,y =250)
    tk.Label(idFrame, text = f"Favourite Movie:", font = ('MS Gothic', 20), bg="snow", fg="grey1").place(x= 0, y = 300)
    with open("YourFav.json", "r") as file:
        data = json.load(file)
        title = data.get("primaryTitle")
        interest = data.get("interests", [])
        jInterest = []
        jInterestID = []
        for i in interest:
            if i.get("isSubgenre") == True:
                jInterest.append(i.get("name"))
                jInterestID.append(i.get("id"))
            if len(jInterest )==2:
                break
    tk.Label(idFrame, text = title, font = ('MS Gothic', 20), bg="snow", fg="grey1").place(x= 0, y = 350)
   
    selected_ids = []
    if position is not None:
        selected_ids.append(idArray[position])
    for mid in idArray:
        if mid not in selected_ids:
            selected_ids.append(mid)
        if len(selected_ids) >= 4:
            break

    poster_size = (230, 350)
    poster_positions = [(20, 140), (720, 140), (20, 520), (720, 520)]
    for i in range(min(4, len(selected_ids))):
        pil_img = MOVIE_IMAGE_CACHE.get(selected_ids[i], _PLACEHOLDER_IMAGE)
        photo = ImageTk.PhotoImage(pil_img.resize(poster_size, Image.Resampling.LANCZOS))
        rootQuiz._image_references.append(photo)
        x, y = poster_positions[i]
        tk.Label(rootQuiz, image=photo, bg="snow", borderwidth=5,relief = "solid", highlightthickness=0).place(x=x, y=y)
    global Review
    Review = None
    reviewVar = tk.StringVar(value="")
    #tk.Label(idFrame, text = "", font = ('MS Gothic', 20), bg="snow", fg="grey1").place(x= 0, y = 400)
    tk.Label(idFrame, text = "Do reviews and ratings influence your movie choices?", font = ('MS Gothic', 20), bg="snow", fg="grey1",wraplength = 400).place(x= 30, y = 400)
    cbxReviewYes = tk.Radiobutton(idFrame, text = "Yes", font = ('MS Gothic', 20), bg="snow", fg="grey1", variable=reviewVar, value="yes")
    cbxReviewYes.place(x= 150, y = 500)
    cbxReviewNo = tk.Radiobutton(idFrame, text = "No", font = ('MS Gothic', 20), bg="snow", fg="grey1", variable=reviewVar, value="no")
    cbxReviewNo.place(x= 150, y = 540)
    tk.Label(idFrame, text = "Which era of movies do you usually enjoy most?", font = ('MS Gothic', 20), bg="snow", fg="grey1",wraplength = 400).place(x= 2, y = 600)
    eraVar = tk.StringVar(value="")
    cbxEra1 = tk.Radiobutton(idFrame, text = "Classic or Older films", font = ('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar, value="classic")
    cbxEra1.place(x= 0, y = 670)
    cbxEra2 = tk.Radiobutton(idFrame, text = "Late 90s-2000s", font = ('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar, value="late_90s_2000s")
    cbxEra2.place(x= 0, y = 720)
    cbxEra3 = tk.Radiobutton(idFrame, text = "Modern", font = ('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar, value="modern")
    cbxEra3.place(x= 0, y = 770)
    cbxEra4 = tk.Radiobutton(idFrame, text = "Era doesn't matter", font = ('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar, value="any")
    cbxEra4.place(x= 0, y = 820)
    global genre_name
    genre_idx = genre_index if 0 <= genre_index < len(genre) else 0
    genre_name = genre[genre_idx]
    print(f"{genre_name},{jInterest}" )
    subVar = tk.StringVar(value="")
    if len(jInterest) >= 2:
        tk.Label(idFrame, text=f"You like {genre_name}, but are you more drawn to {jInterest[0]} or {jInterest[1]}?", font=('MS Gothic', 20), bg="snow", fg="grey1", wraplength=395).place(x=2, y=900)
        cbxSubYes = tk.Radiobutton(idFrame, text=jInterest[0], font=('MS Gothic', 20), bg="snow", fg="grey1", variable=subVar, value=jInterestID[0])
        cbxSubYes.place(x=0, y=1040)
        cbxSub = tk.Radiobutton(idFrame, text=jInterest[1], font=('MS Gothic', 20), bg="snow", fg="grey1", variable=subVar, value=jInterestID[1])
        cbxSub.place(x=0, y=1090)
    else:
        tk.Label(idFrame, text=f"You like {genre_name}.", font=('MS Gothic', 20), bg="snow", fg="grey1", wraplength=395).place(x=2, y=900)
    tk.Label(idFrame, text="How important is pacing to you?", font=('MS Gothic', 20), bg="snow", fg="grey1", wraplength=400).place(x=0, y=1150)
    eraVar2 = tk.StringVar(value="")
    cbxEra1 = tk.Radiobutton(idFrame, text="Short and easy to watch", font=('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar2, value="short")
    cbxEra1.place(x=0, y=1220)
    cbxEra2 = tk.Radiobutton(idFrame, text="Medium length", font=('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar2, value="medium")
    cbxEra2.place(x=0, y=1280)
    cbxEra3 = tk.Radiobutton(idFrame, text="Long and immersive", font=('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar2, value="long")
    cbxEra3.place(x=0, y=1350)
    cbxEra4 = tk.Radiobutton(idFrame, text="Length doesn't matter", font=('MS Gothic', 20), bg="snow", fg="grey1", variable=eraVar2, value="any")
    cbxEra4.place(x=0, y=1400)

    def on_submit():
        global Age, Name, EndYear, Review,interests, length, StartYear, genre_name, startLength
        Age = sedtAge.get()
        Name = edtName.get()
        Review = reviewVar.get()
        if Review == "yes":
            Review = True
        else:
            Review = False
        choice = eraVar.get()
        interests = subVar.get()
        if choice == "classic":
            StartYear, EndYear = 1800, 1995
        elif choice == "late_90s_2000s":
            StartYear, EndYear = 1996, 2010
        elif choice == "modern":
            StartYear, EndYear = 2011, 2025
        else:
            StartYear, EndYear = None, None
        choice = eraVar2.get()
        if choice == "short":
            startLength, length = 0, 60*60
        elif choice == "medium":
            startLength, length = 60*60, 120*60
        elif choice == "long":
            startLength, length = 120*60, 180*60
        else:
            startLength, length = None, None
        print(f"{Age}, {Name}, {Review}, {choice}, {startLength}, {length}, {interests}, {StartYear}, {EndYear}")
        FinalMovie()

    EnterButton = tk.Button(idFrame, text="Enter", font=('MS Gothic', 20), bg="snow", fg="grey1", command=on_submit)
    EnterButton.place(x=0, y=1580)
    rootQuiz.bind("<Return>", lambda e: on_submit())

    def on_mousewheel(event):
        if event.delta:
            # Windows
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            # Linux
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
    
    def bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>", on_mousewheel)
        canvas.bind_all("<Button-5>", on_mousewheel)
    
    def unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
    
    canvas.bind("<Enter>", bind_mousewheel)
    canvas.bind("<Leave>", unbind_mousewheel)
    
  
    def force_frame_update():
        rootQuiz.update_idletasks()
        canvas.update_idletasks()
  
        required_height = 1600
        scrollable_frame.config(width=390, height=required_height)
      
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    
    rootQuiz.after(50, force_frame_update)  
    rootQuiz.update_idletasks()  
    
    rootQuiz.mainloop()

Image.MAX_IMAGE_PIXELS = 200000000
_PLACEHOLDER_IMAGE = Image.new("RGB", (250, 375), (40, 40, 60))


MOVIE_IMAGE_CACHE = {}  

def MoviePic(index):
    global idArray, root3, genre_index
    genre_index = index
    idArray = []
    arrMovieTitle = []
    movie_ids = []
    root2.destroy()
    root3 = tk.Tk()
    root3.title("Movie Recommendations")
    root3.geometry("1250x1000")
    root3.config(bg="tomato1")
    root3._tk_images = []
    root3.resizable(False,False)
    canvas = tk.Canvas(root3, bg="tomato1", highlightthickness=0)
    scrollbar = tk.Scrollbar(root3, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)
    container = tk.Frame(canvas, bg="tomato1")
    canvas_window = canvas.create_window((0, 0), window=container, anchor="nw")
    tk.Label(container, text="Which of these movies do you like most?", 
             font=('Haettenschweiler', 36), bg="snow", fg="grey1").pack(pady=20)
    
    
    loading_label = tk.Label(container, text="Loading movies...", 
                            font=('Arial', 18), bg="tomato1", fg="snow")
    loading_label.pack(pady=20)
    root3.update()
    

    genre_id = TMDB_GENRES.get(genre[index], "")
    paramaters = {
        "with_genres": str(genre_id),
        "sort_by": "popularity.desc",
        "primary_release_date.lte": "2025-12-31"
    }
    
    try:
        titleFile = getMovies(paramaters)
        readTitles = titleFile.get("titles", [])
        
        
        def write_json_file():
            try:
                with open("titleFile.json", 'w') as file:
                    json.dump(titleFile, file, indent=3)
            except Exception as e:
                print(f"Error writing JSON file: {e}")
        
        threading.Thread(target=write_json_file, daemon=True).start()
    except Exception as e:
        print(f"Error fetching movies: {e}")
        readTitles = []
    
    if not readTitles:
        loading_label.destroy()
        tk.Label(container, text="No movies found!", 
                font=('Arial', 24), bg="tomato1", fg="snow").pack(pady=50)
        canvas.configure(scrollregion=canvas.bbox("all"))
        root3.mainloop()
        return
    
    def load_image_data(image_url):
        """Load image data from URL in a thread-safe way"""
        if not image_url:
            return None
        
        try:
            with urllib.request.urlopen(image_url, timeout=10) as u:
                data = u.read()
            img = Image.open(io.BytesIO(data))
            return img
        except Exception as e:
            print(f"Error loading image {image_url}: {e}")
            return None
    
    def create_photo_image(img_data):
        """Convert PIL Image to PhotoImage (must be called from main thread)"""
        if img_data is None:
            return ImageTk.PhotoImage(_PLACEHOLDER_IMAGE)
        try:
            img_resized = img_data.resize((250, 375), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img_resized)
        except Exception as e:
            print(f"Error processing image: {e}")
            return ImageTk.PhotoImage(_PLACEHOLDER_IMAGE)
    
    grid_frame = tk.Frame(container, bg="tomato1")
    grid_frame.pack(pady=(0, 20), padx=10)

    num_movies = min(8, len(readTitles))
    selected_movies = random.sample(readTitles, num_movies)
    
   
    movie_frames = []
    
    for i, movie in enumerate(selected_movies):
        movie_id = movie.get("id")
        movie_title = movie.get("primaryTitle", "Unknown")
        image_url = movie.get("primaryImage", {}).get("url", "")
        
        idArray.append(movie_id)
        arrMovieTitle.append(movie_title)
        movie_ids.append(movie_id)
        
        row, col = divmod(i, 4)
        movie_frame = tk.Frame(grid_frame, bg="tomato1")
        movie_frame.grid(row=row, column=col, padx=20, pady=10, sticky="n")
        movie_frames.append((movie_frame, image_url, movie_title, i))
    
    loading_label.destroy()
    
  
    def load_images_async():
        with ThreadPoolExecutor(max_workers=4) as executor:
           
            future_to_index = {}
            for idx, (movie_frame, image_url, movie_title, i) in enumerate(movie_frames):
                future = executor.submit(load_image_data, image_url)
                future_to_index[future] = (idx, movie_frame, movie_title, i)
            
   
            for future in as_completed(future_to_index):
                idx, movie_frame, movie_title, i = future_to_index[future]
                img_data = future.result()
                movie_id = movie_ids[idx] if idx < len(movie_ids) else None
                if movie_id and img_data is not None:
                    MOVIE_IMAGE_CACHE[movie_id] = img_data
                
                
                root3.after(0, lambda idx_val=idx, frame_val=movie_frame, title_val=movie_title, 
                           img_val=img_data, btn_idx_val=i: create_movie_widget(
                           idx_val, frame_val, title_val, img_val, btn_idx_val))
    
    def create_movie_widget(idx, movie_frame, movie_title, img_data, btn_idx):
        """Create movie button and label widget (called from main thread)"""
        tk_image = create_photo_image(img_data)
        root3._tk_images.append(tk_image)
        
        btn = tk.Button(movie_frame, image=tk_image, bd=5, bg="tomato1",
                       activebackground="tomato1", highlightthickness=0, 
                       relief="solid", command=lambda idx=btn_idx: Quiz(idx))
        btn.pack()
        tk.Label(movie_frame, text=movie_title, font=('Haettenschweiler', 25),
                bg="snow", fg="black", wraplength=250).pack(pady=(5, 0))
        
        
        root3.after_idle(lambda: canvas.configure(scrollregion=canvas.bbox("all")))


    threading.Thread(target=load_images_async, daemon=True).start()

    tk.Label(container, text="Click on any movie poster to continue",
            font=('Arial', 12), bg="snow", fg="grey1").pack()
            
    def update_scroll(event=None):
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def update_canvas_width(event):
        canvas.itemconfig(canvas_window, width=event.width)

    container.bind("<Configure>", update_scroll)
    canvas.bind("<Configure>", update_canvas_width)

    root3.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    root3.mainloop()
def Start():
    global genre
    genre = ["Action", "Adventure", "Animation", "Comedy", "Documentary", "Drama", "Fantasy","Horror","Sci-Fi","Thriller"]
    #int Index
    root.destroy()
    global root2
    root2 = tk.Tk()
    root2.geometry("1350x750")
    root2.config(bg = "tomato1")
    #root2.attributes('-alpha', 0.7)
   
    root2.resizable(False, False)
    lblChoose = tk.Label(root2, text = "Please choose" ,font=('Haettenschweiler', 36))
    lblChoose.place(x=10,y=10)
    lblChoose2 = tk.Label(root2,text ="any genre you’re",font=('Haettenschweiler', 36) )
    lblChoose2.place(x = 10, y = 80)
    lblChoose3 = tk.Label(root2,text = "interested in.",font=('Haettenschweiler', 36) )
    lblChoose3.place(x = 10,y =150)
   
    script_dir = os.path.dirname(os.path.abspath(__file__))
   
    y_start = 240  
    spacing = 70   
    index = 0
    for i, g in enumerate(genre):
        frame = tk.Frame(root2, width=200, height=60)
        frame.pack_propagate(False)
        frame.place(x=40, y=y_start + i * spacing)
        btn = tk.Button(frame, text=g, font=('Haettenschweiler', 36), command=lambda idx_val=index: MoviePic(idx_val))
        index =  index +1
        btn.pack(fill="both", expand=True)
        if i == 6:
            break;
    k = 0
    
    for i in range(7,10):
        frame = tk.Frame(root2, width=200, height=60)
        frame.pack_propagate(False)
       
        frame.place(x=1130, y=10+k* spacing)
        k = k+1
        btn = tk.Button(frame, text=genre[i], font=('Haettenschweiler', 36), command=lambda idx_val=i: MoviePic(idx_val))
        btn.pack(fill="both", expand=True)  

 
    poster_data = [{"filename": "Akira.png", "x": 310, "y": 0},
    {"filename": "Taxi Driver (1976).png", "x": 570, "y": 0},
    {"filename": "Breaking Bad (2008).png", "x": 830, "y": 0},
    {"filename": "RoboCop (1987).jpeg", "x": 310, "y": 370},
    {"filename": "The Muppet Movie (1979).png", "x": 830, "y": 370},
    {"filename": "Pulp Fiction (1994).png", "x": 570, "y": 370},]

    global width
    width = 230
    global height
    height = 350
    root2._image_references = []
    for item in poster_data:
        image_path = os.path.join(script_dir, "images", item["filename"])
        imgPoster1 = Image.open(image_path)
        imgPoster1 = imgPoster1.resize((width,height),Image.Resampling.LANCZOS)
        tk_image =  ImageTk.PhotoImage(imgPoster1)
        image_label = tk.Label(root2, image=tk_image, bd = 5, relief = "solid")
        image_label.image = tk_image
        image_label.place(x=item["x"], y = item["y"])
        root2._image_references.append(tk_image)


    root2.mainloop()

def options():
    ...
def getTime():  
    user_locale = locale.getlocale()
    try:
        locale.setlocale(locale.LC_TIME, user_locale)
    except locale.Error:
        print(f'locale {user_locale} is not supported')
        locale.setlocale(locale.LC_TIME, 'C')
    global today
    today = datetime.now()
    t = today.time()
    return f'{today:%x}, {t:%X}'

def updateClock():
    label3.config(text=getTime())
    label3.after(1000, updateClock)


def getMovies(param):
    param["api_key"] = TMDB_API_KEY
    param["include_adult"] = "false"
    param["language"] = "en-US"
    
    response = requests.get("https://api.themoviedb.org/3/discover/movie", params=param)
    raw_data = response.json()
    
  
    mapped_movies = []
    for m in raw_data.get("results", []):
        year = m.get("release_date", "")[:4]
        mapped_movies.append({
            "id": m.get("id"),
            "primaryTitle": m.get("title"),
            "plot": m.get("overview"),
            "startYear": year,
            "runtimeSeconds": 100 * 60, 
            "primaryImage": {
                "url": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}" if m.get('poster_path') else ""
            }
        })
        
    return {"titles": mapped_movies}
    
def main():
    global root
    root = tk.Tk()
    root.geometry("1000x700")
    root.title("Movie APis ") 
    root.resizable(False, False)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "images", "MainMenu.jpg")
    imgMenu = Image.open(image_path)
    imgMenu = imgMenu.resize((1920,1080),Image.Resampling.LANCZOS)
    tk_image =  ImageTk.PhotoImage(imgMenu)
    image_label = tk.Label(root, image=tk_image)
    image_label.pack()
    image_label.image = tk_image
    label2 = tk.Label(root, text="yellow", font=("Helvetica", 30), bg = "black", fg = "white")
    label2.pack()
    global label3
    label3 = tk.Label(image_label, text=getTime(), font=("Helvetica", 48), bg = "black", fg = "white")
    label3.pack()
    label3.place(x=140, y =248)
    label4 = tk.Label(image_label, text = "Movie Recomondations" , font = ("Led Italic Font", 25), bg ="coral2")
    label4.pack()
    label4.place(x =108, y= 342)
    frame = tk.Frame(image_label, width=200, height=60)
    frame.pack_propagate(False)
    frame.place(x = 110, y = 430)
    button1 = tk.Button (frame, text = "Start", font=('Mistral', 50), command = Start, bg = "gold2")
    button1.pack(fill = "both", expand = True)
    frame2 = tk.Frame(image_label, width=200, height=60)
    frame2.pack_propagate(False)
    frame2.place(x = 430, y = 430)
    button2 = tk.Button(frame2,text = "Options" ,font=('Haettenschweiler', 40), command = options, bg ="cornflower blue")
    button2.pack(fill = "both", expand = True)


    updateClock()


    root.mainloop()

if __name__ == "__main__":
    main()
