export const generateUrl = (part: string) => {
    return `${process.env.REACT_APP_BACKEND_PROTOCOL || "http"}://${
        process.env.REACT_APP_BACKEND_LINK || "localhost:8000"
    }/api/v1/${part.replace(/^\/+/, "")}`;
};
