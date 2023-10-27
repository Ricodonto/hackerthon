import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// import App from './App';
import reportWebVitals from './reportWebVitals';
// Stuff for routing, we'll be using react router
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

// Importing the content of each or our routes
import About from './About/page';
import History from './History/page';
import Home from './Home/page';
import Login from './Login/page';
import Response from './Response/page';
import SignUp from './SignUp/page';
import ErrorPage from './Error/page';
import Root from './Root/page';

// Defining routes
const router = createBrowserRouter([
  // Each route is defined as the path of the route and the content to show on that route, we're defining data routes
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Home />
      },
      {
        path: "about",
        element: <About />
      },
      {
        path: "history",
        element: <History />
      },
      {
        path: "response",
        element: <Response />
      },
    ]
  },
  {
    path: "signup",
    element: <SignUp />,
    errorElement: <ErrorPage />,
  },
  {
    path: "login",
    element: <Login />,
    errorElement: <ErrorPage />,
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
