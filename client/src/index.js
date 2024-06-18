import React from "react";
import ReactDOM from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import "./index.css";
import 'bootstrap/dist/css/bootstrap.min.css';

import Home from "./pages/Home";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Profile from "./pages/Profile";
import Opportunities from "./pages/Opportunities";
import ErrorPage from './pages/ErrorPage';

const routes = [
    {
        path:'/',
        element: <Home />,
        errorElement: <ErrorPage />
    },
    // {
    //     path: '/home',
    //     element:<Home />,
    //     errorElement: <ErrorPage />
    // },
    {
        path:'/login',
        element: <Login />,
        errorElement: <ErrorPage />
    },
    {
        path:'/signup',
        element: <SignUp />,
        errorElement: <ErrorPage />
    },
    {
        path:'/profile',
        element: <Profile />,
        errorElement: <ErrorPage />
    },
    {
        path:'/opportunities',
        element: <Opportunities />,
        errorElement: <ErrorPage />
    },
    

]

const router = createBrowserRouter(routes)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <RouterProvider router={router}/>
    </React.StrictMode>
);
