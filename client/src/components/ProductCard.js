import React from "react";

const ProductCard = ({ prodDetails, setReport, setLoading }) => {
    const handleClick = () => {
        setLoading(true);
        setReport(null);

        fetch(`http://localhost:8000/analyse?q=${prodDetails.search_term}`)
            .then((response) => response.json())
            .then((data) => {
                setReport(data);

                setLoading(false);
            });
    };

    return (
        <div className="prod-container">
            <div className="prod-img">
                <img src={prodDetails.img} />
            </div>
            <div className="prod-info">
                <h1 className="prod-name">{prodDetails.name}</h1>
                <h3 className="prod-price">{prodDetails.price}</h3>
                <button className="analyse-btn" onClick={handleClick}>
                    Get analysis
                </button>
            </div>
        </div>
    );
};

export default ProductCard;
