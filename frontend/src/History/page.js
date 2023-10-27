import { useState } from 'react';
import './styles.css';
import { AiFillDelete } from 'react-icons/ai';
import { MyButton } from '../Home/page';

export default function History() {
    const [histories, setHistories] = useState([
        {
            description: "Harry Potter and the Philosopher's Stone is a fantasy novel written by British author J. K. Rowling",
            title: "Harry Potter and the Sorcerer's Stone",
            author: "J. K. Rowling",
            rating: 4.6,
            imageUrl: "https://covers.openlibrary.org/b/id/13741661-M.jpg",
            moreInfoLink: "https://openlibrary.org/works/OL34924410W/Harry_Potter_And_The_Sorcer%27s_Stone?edition=key%3A/books/OL7893441M"
        }
    ]);

    function handleDelete(i) {
        let newHistories = histories.slice();
        newHistories.splice(i, 1)
        setHistories(newHistories);
    }

    function deleteAllHistory() {
        setHistories([]);
    }

    return (
        <main>
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
        </main>
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