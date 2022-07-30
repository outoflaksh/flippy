import React from "react";
import { useRef } from "react";

const ProductSearch = ({ setProdDetails }) => {
    const inputRef = useRef(null);

    const handleClick = () => {
        fetch(
            `http://localhost:8000/details?prod_url=${inputRef.current.value}`
        )
            .then((response) => response.json())
            .then((data) => setProdDetails(data));
    };

    return (
        <div className="search">
            <input
                type="text"
                placeholder="Enter Flipkart product URL here"
                className="search-box"
                ref={inputRef}
            />
            <button className="search-btn" onClick={handleClick}>
                Get details
            </button>
        </div>
    );
};

export default ProductSearch;
