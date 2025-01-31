import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { generateUrl } from "../utils/generateUrl";

type ListProps = {
    url: string;
    addUrl?: string;
    targetValue: string;
    navigationPrefix: string;
};

const List = ({ url, addUrl, targetValue, navigationPrefix }: ListProps) => {
    const navigate = useNavigate();
    const [items, setItems] = useState<any>([]);

    useEffect(() => {
        const getItems = async () => {
            await axios
                .get(generateUrl(url))
                .then((res: any) => setItems(res.data))
                .catch(() => toast.error("Не удалось получить список 😢"));
        };

        getItems();
    }, [url]);

    return (
        <div className="profiles-list-container">
            {addUrl && (
                <svg
                    onClick={() => navigate(addUrl)}
                    style={{ cursor: "pointer" }}
                    xmlns="http://www.w3.org/2000/svg"
                    width="30px"
                    viewBox="0 0 24 24"
                    fill="none"
                >
                    <circle
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="#fff"
                        stroke-width="1.5"
                    />
                    <path
                        d="M15 12L12 12M12 12L9 12M12 12L12 9M12 12L12 15"
                        stroke="#fff"
                        stroke-width="1.5"
                        stroke-linecap="round"
                    />
                </svg>
            )}
            <div className="profiles-list">
                {items &&
                    items.length > 0 &&
                    items.map((item: any) => (
                        <div
                            className="profile"
                            onClick={() =>
                                navigate(`${navigationPrefix}/${item.id}`)
                            }
                        >
                            {item[targetValue]}
                        </div>
                    ))}
            </div>
        </div>
    );
};

export default List;
