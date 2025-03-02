import { SET_AUTH } from "./authActionTypes";

const initialState = {
    isAuth: false,
};

export const AuthReducer = (state = initialState, action: any) => {
    switch (action.type) {
        case SET_AUTH:
            return { ...state, isAuth: action.payload };
        default:
            return state;
    }
};
