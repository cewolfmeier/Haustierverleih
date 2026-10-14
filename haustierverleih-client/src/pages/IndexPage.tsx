export default function IndexPage(){
    return (
        <>
        <a href="/">        
            <img className="title-image" src="/logo.png" alt="Das Logo des Haustierverleihs" />
        </a> 
        <h1>Willkommen beim Haustierverleih!</h1> {/* 
        <ul className="content-list">
            {% for pet in pets %}
            <a href="{{url_for('main.pet', pet_id=pet.pet_id)}}">
            <li className="shadow">
                {% if pet.image %}
                <img className="thumbnail" src="{{ url_for('static', filename='images/user_uploads/'+pet.image)}}" alt="">
                {% else %}
                <img className="thumbnail" src="{{ url_for('static', filename='images/logo-thumbnail.png')}}" alt="">
                {% endif %}
                <div>
                    <h2>{{ pet.name }} ({{ pet.animal_type.animal_type }})</h2>
                    {% if pet.borrower_id %}
                    <div className="badge dark shadow">Nicht verfügbar</div>
                    {% else %}
                    <div className="badge success shadow">Aktuell verfügbar</div>
                    {% endif %}
                </div>
                <div>
                    <div className="description">{{ pet.description }}</div>
                    <div>{{ pet.name }} gehört {{ pet.owned }}</div>
                    
                </div>
            </li>
            </a>
            {% endfor %}
        </ul>
            */}
    </>
    );
};