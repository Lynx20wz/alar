# What is Alar?  

Alar is a full-stack web application created as a pet project. It's an attempt to combine GitHub and Reddit, like "Reddit for programmers."

## ✨ Features

### ✅ Implemented

- ([00e9](https://github.com/Lynx20wz/alar/commit/00e993057963ef9b52ae8915be87d4f5db6f2bfc)) **Authentication System** - Secure JWT-based auth
- ([cf0c](https://github.com/Lynx20wz/alar/commit/cf0c9414bfb25ddd2dfd378ed8b6f65e1dc0dcea)) **Posts** - Create, read, and engage with content
- ([cf0c](https://github.com/Lynx20wz/alar/commit/cf0c9414bfb25ddd2dfd378ed8b6f65e1dc0dcea)) **Comments** - Nested discussions on posts

### 🚧 In Progress

- **User Profiles** - Personalized profile pages
- **Notifications** - Real-time updates and alerts
- **Search** - Advanced content discovery
- **Question Posts** - StackOverflow-style Q&A
- **Code Snippets** - GitHub Gists-like code sharing
- **Dockerization** - Containerized deployment
- **Production Deployment** - Cloud deployment setup

## Tech stack

### Frontend

- **TypeScript** - Strongly typed programming language
- **SvelteKit** - Lightweight framework for building modern web apps
- **SCSS** - CSS preprocessor

### Backend

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM (planned to switch to [SQLmodel](https://sqlmodel.tiangolo.com/))
- **SQLite** - Development database (planned to switch to [PostgreSQL](https://www.postgresql.org/))

## Project Structure

```bash
Alar/
├───README.md  # Project documentation and overview
├───back/      # --Backend (FastAPI application)--
│   ├───apis/  # --API routes and endpoints--
│   │   ├───auth.py      # Authentication and authorization routes
│   │   ├───comments.py  # Comment management endpoints
│   │   ├───posts.py     # Post creation and retrieval endpoints  
│   │   └───users.py     # User profile and management endpoints
│   ├───database/  # --Database layer and models--
│   │   ├───models/  # --SQLAlchemy ORM models--
│   │   │   ├───UserModel.py        # User table model
│   │   │   ├───PostModel.py        # Post table model
│   │   │   ├───CommentModel.py     # Comment table model
│   │   │   ├───SocialLinkModel.py  # Social link table model
│   │   │   ├───StackModel.py       # Social link table model
│   │   │   └───LikedModel.py       # Like table model
│   │   ├───core.py  # Database base class and session setup
│   │   └───crud.py  # CRUD operations
│   ├───schemas.py  # Pydantic schemas for request/response validation
│   ├───deps.py     # FastAPI dependencies
│   ├───jwt.py      # JWT token generation and validation utilities
│   └───main.py     # FastAPI application entry point
│
└───front/  # Frontend (SvelteKit application)
    ├───src/  # --Frontend source code--
    │   ├───lib/  # --Reusable utilities and components--
    │   │   ├───components/  # --UI components--
    │   │   │   ├───Alert.svelte     # Notification and message alerts
    │   │   │   ├───Aside.svelte     # Sidebar navigation component
    │   │   │   ├───Header.svelte    # Main header with navigation
    │   │   │   ├───Post.svelte      # Post display component
    │   │   │   └───UserCard.svelte  # User profile card component
    │   │   ├───stores/  # --State management stores--
    │   │   │   └───userStore.ts   # Global user state management
    │   │   └───types/  # --TypeScript type definitions--
    │   │       ├───Comment.ts  # Comment-related interfaces
    │   │       ├───Likes.ts    #Like and engagement interfaces  
    │   │       ├───Others.ts   # Utility and shared interfaces
    │   │       ├───Post.ts     # Post-related interfaces
    │   │       └───User.ts     # User profile interfaces
    │   ├───public/   # --Static assets--
    │   │   ├───fonts/  # Custom font files
    │   │   └───i18n/   # Internationalization files
    │   └───routes/  # --Page routes and layouts--
    │       ├───[username]/  # --Dynamic user profile pages--
    │       │   ├───+page.svelte  # User profile view
    │       │   └───+page.ts      # User data loading
    │       ├───login/  # --Authentication page--
    │       │   └───+page.svelte   # Login form component
    │       ├───post/  # --Post-related pages--
    │       │   └───[postId]/   # Dynamic post detail pages
    │       │       ├───+page.svelte  # Post detail view
    │       │       └───+page.ts      # Post data loading
    │       ├───registration/  # --User registration page--
    │       │   └───+page.svelte   # Registration form component
    │       └───styles/  # --Global styles and CSS--
    │           ├───_fonts.scss      # Custom font definitions
    │           ├───_normalize.scss  # CSS reset and normalization
    │           ├───_themes.scss     # Color and theme definitions
    │           └───global.scss      # Global styles and variables
    └───static/  # --Build-time static files--
        ├───robots.txt   # Search engine crawler instructions
        └───favicon.png  # Website favicon
```

## 🔗 API Documentation

Once running, explore the auto-generated API docs at:

OpenAPI (Swagger) UI: <http://localhost:8000/docs>
ReDoc: <http://localhost:8000/redoc>
