import './styles.css';

export default function About() {
    return (
        <main>
            <h2>About BookFinder</h2>
            <p>Welcome to Bookfinder, your go-to online book recommender designed for students and book enthusiasts alike.</p>
            <p>With Bookfinder, you can simply ask for book recommendations and get personalized suggestions tailored to your interests and preferences.</p>
            <p>Our goal is to offer a seamless and enjoyable user experience through:</p>
            <section>
                <AboutSection 
                    title={"User-Friendly Platform:"}
                    sentence1={"We're creating a user-friendly website that makes Bookfinder easily accessible to everyone."}
                    sentence2={"You can effortlessly enter your book recommendation request, no matter your level of tech-savviness."}
                />
                <AboutSection 
                    title={"Curated Book Lists:"}
                    sentence1={"Bookfinder will generate a list of approximately five books that align with your request."}
                    sentence2={"We'll also dive into a database, aided by OpenAI plugins, to fetch additional details such as the number of pages, ISBN, publication date, book cover images, ratings, and more."}
                    left={true}
                />
                <AboutSection 
                    title={"Concise Book Details:"}
                    sentence1={"We'll present the recommended books and their essential details in a brief and informative paragraph."}
                    sentence2={"This allows you to quickly assess which book might be your next literary adventure."}
                />
            </section>
        </main>
    );
}

function AboutSection(props) {
    if (props.left === true) {
        return (
            <div className='about-section-left'>
                <div>
                    <h3>{props.title}</h3>
                    <p>{props.sentence1}</p>
                    <p>{props.sentence2}</p>
                </div>
                <img></img>
            </div>
        );
    }
    return (
        <div className='about-section'>
            <img></img>
            <div>
                <h3>{props.title}</h3>
                <p>{props.sentence1}</p>
                <p>{props.sentence2}</p>
            </div>
        </div>
    );
}