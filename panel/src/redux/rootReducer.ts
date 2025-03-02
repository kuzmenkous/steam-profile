import { combineReducers } from "@reduxjs/toolkit";
import { AuthReducer } from "./auth/authReducer";

export const RootReducer = combineReducers({
    AuthReducer,
});
