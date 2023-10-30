import { useState } from 'react';
import './styles.css';
import { AiFillDelete } from 'react-icons/ai';
import { MyButton } from '../Home/page';
import { useLoaderData } from 'react-router-dom';
import ErrorWidget from '../Components/errorWidget';
import LoadingScreen from '../Components/loadingScreen';

export default function History() {
    const originalHistories = useLoaderData();
    const [histories, setHistories] = useState(originalHistories);
    const [error, setError] = useState(false);
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [loadingMessage, setLoadingMessage] = useState("");

    function handleDelete(i) {
        let newHistories = histories.slice();
        newHistories.splice(i, 1)
        setHistories(newHistories);
    }

    function deleteAllHistory() {
        setHistories([]);
    }

    if (loading === true) {
        return <ErrorWidget message={errorMessage} />;
    } else if (error === true) {
        return <LoadingScreen message={loadingMessage} />;
    }
    return (
        <div className='content-page'>
            <div className='history'>
                <h2>History</h2>
                <MyButton text={"Delete History"} 
                    delete={true}
                    handleClick={deleteAllHistory}
                />
            </div>
            <section>
                {histories.map((val, index) => {
                    return <SearchResult
                        key={index}
                        imageUrl={val.imageUrl}
                        title={val.title}
                        author={val.author}
                        rating={val.rating}
                        description={val.description}
                        moreInfoLink={val.moreInfoLink}
                        deleteHistory={() => handleDelete(index)}
                    />
                })}
            </section>
        </div>
    );
}

function SearchResult(props) {
    return (
        <div className='search-result'>
            <img className='search-image' src={props.imageUrl}></img>
            <p style={{ flex: 2 }}>{props.title}</p>
            <p style={{ flex: 2 }}>{props.author}</p>
            <p style={{ flex: 1 }}>{props.rating}</p>
            <p style={{ flex: 3 }}>{props.description}</p>
            <MyButton text={'More Info'}
                handleClick={() => {
                    window.open(props.moreInfoLink, "_blank")
                }}
            />
            <AiFillDelete style={{ color: "red" }} onClick={props.deleteHistory} />
        </div>
    );
}