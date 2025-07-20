#!/usr/bin/env python
"""
Script pentru generarea de articole pentru blog
"""
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_board.settings')
django.setup()

from core.models import Article
from accounts.models import User

def create_articles():
    """Creează 10 articole pentru blog"""
    
    # Găsește primul superuser sau creează unul
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            print("Nu s-a găsit niciun utilizator admin. Creez unul...")
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@joburiexpress.ro',
                password='admin123',
                user_type='admin'
            )
    except Exception as e:
        print(f"Eroare la găsirea/crearea utilizatorului admin: {e}")
        return

    articles_data = [
        {
            'title': 'Cum să îți scrii un CV perfect în 2025',
            'excerpt': 'Descoperă secretele unui CV care atrage atenția recruiterilor și te ajută să obții jobul dorit.',
            'content': '''
            <h2>Introducere</h2>
            <p>Un CV bine structurat este cheia succesului în căutarea unui loc de muncă. În 2025, recrutorii petrec în medie doar 6 secunde citind un CV, așa că fiecare detaliu contează.</p>
            
            <h2>Structura ideală a unui CV</h2>
            <h3>1. Informații de contact</h3>
            <p>Include numele complet, numărul de telefon, adresa de email profesională și profilul LinkedIn.</p>
            
            <h3>2. Rezumatul profesional</h3>
            <p>Un paragraf scurt (2-3 propoziții) care rezumă experiența și obiectivele tale profesionale.</p>
            
            <h3>3. Experiența profesională</h3>
            <p>Listează joburile în ordine cronologică inversă, cu accent pe realizări măsurabile.</p>
            
            <h3>4. Educația</h3>
            <p>Include studiile relevante, certificările și cursurile importante.</p>
            
            <h3>5. Competențe</h3>
            <p>Menționează competențele tehnice și soft skills relevante pentru poziția dorită.</p>
            
            <h2>Sfaturi pentru optimizare</h2>
            <ul>
                <li>Folosește cuvinte cheie din anunțul de job</li>
                <li>Păstrează CV-ul la maximum 2 pagini</li>
                <li>Folosește un design curat și profesional</li>
                <li>Verifică ortografia și gramatica</li>
            </ul>
            
            <h2>Concluzie</h2>
            <p>Un CV excelent este investiția ta în viitorul profesional. Dedică timp pentru a-l perfecționa și vei vedea rezultate pozitive în căutarea jobului.</p>
            ''',
            'is_featured': True
        },
        {
            'title': 'Top 10 competențe digitale căutate de angajatori',
            'excerpt': 'Află care sunt competențele digitale cele mai valoroase pe piața muncii și cum să le dezvolți.',
            'content': '''
            <h2>Competențele digitale - necesitate în era modernă</h2>
            <p>În lumea digitală de astăzi, competențele tehnologice nu mai sunt opționale. Iată top 10 competențe digitale căutate de angajatori:</p>
            
            <h2>1. Analiza datelor</h2>
            <p>Capacitatea de a interpreta și analiza date pentru a lua decizii informate.</p>
            
            <h2>2. Marketing digital</h2>
            <p>Cunoștințe de SEO, social media marketing, Google Ads și email marketing.</p>
            
            <h2>3. Programare</h2>
            <p>Limbaje precum Python, JavaScript, Java sau C# sunt foarte căutate.</p>
            
            <h2>4. Cybersecurity</h2>
            <p>Protejarea sistemelor și datelor împotriva amenințărilor cibernetice.</p>
            
            <h2>5. Cloud Computing</h2>
            <p>Experiență cu AWS, Azure sau Google Cloud Platform.</p>
            
            <h2>6. Inteligența artificială și Machine Learning</h2>
            <p>Dezvoltarea și implementarea soluțiilor AI.</p>
            
            <h2>7. UX/UI Design</h2>
            <p>Crearea experiențelor digitale intuitive și atractive.</p>
            
            <h2>8. Automatizarea proceselor</h2>
            <p>Optimizarea workflow-urilor prin tehnologie.</p>
            
            <h2>9. E-commerce</h2>
            <p>Gestionarea magazinelor online și platformelor de vânzare.</p>
            
            <h2>10. Colaborarea digitală</h2>
            <p>Utilizarea eficientă a toolurilor de colaborare online.</p>
            
            <h2>Cum să dezvolți aceste competențe</h2>
            <ul>
                <li>Cursuri online (Coursera, Udemy, edX)</li>
                <li>Certificări profesionale</li>
                <li>Proiecte practice</li>
                <li>Mentorat și networking</li>
            </ul>
            ''',
            'is_featured': True
        },
        {
            'title': 'Ghidul complet pentru interviul de angajare',
            'excerpt': 'Pregătește-te perfect pentru interviul de angajare cu sfaturile noastre practice și eficiente.',
            'content': '''
            <h2>Pregătirea pentru interviu</h2>
            <p>Un interviu de succes începe cu o pregătire temeinică. Iată pașii esențiali:</p>
            
            <h2>Înainte de interviu</h2>
            <h3>Cercetează compania</h3>
            <ul>
                <li>Studiază site-ul web al companiei</li>
                <li>Citește despre cultura organizațională</li>
                <li>Înțelege produsele/serviciile oferite</li>
                <li>Verifică știrile recente despre companie</li>
            </ul>
            
            <h3>Pregătește răspunsurile</h3>
            <p>Antrenează-te pentru întrebările comune:</p>
            <ul>
                <li>"Povestește-mi despre tine"</li>
                <li>"De ce vrei să lucrezi aici?"</li>
                <li>"Care sunt punctele tale forte și slabe?"</li>
                <li>"Unde te vezi în 5 ani?"</li>
            </ul>
            
            <h2>În timpul interviului</h2>
            <h3>Limbajul corpului</h3>
            <ul>
                <li>Menține contactul vizual</li>
                <li>Zâmbește natural</li>
                <li>Stai drept și relaxat</li>
                <li>Folosește gesturi deschise</li>
            </ul>
            
            <h3>Comunicarea eficientă</h3>
            <ul>
                <li>Ascultă atent întrebările</li>
                <li>Răspunde clar și concis</li>
                <li>Folosește exemple concrete</li>
                <li>Pune întrebări inteligente</li>
            </ul>
            
            <h2>După interviu</h2>
            <ul>
                <li>Trimite un email de mulțumire în 24 de ore</li>
                <li>Reiterează interesul pentru poziție</li>
                <li>Menționează punctele cheie discutate</li>
                <li>Urmărește răspunsul în termenul stabilit</li>
            </ul>
            ''',
            'is_featured': True
        },
        {
            'title': 'Cum să negociezi salariul la noul job',
            'excerpt': 'Strategii eficiente pentru negocierea salariului și beneficiilor la un nou loc de muncă.',
            'content': '''
            <h2>Pregătirea pentru negociere</h2>
            <p>Negocierea salariului este un proces care necesită pregătire și strategie. Iată cum să abordezi această discuție:</p>
            
            <h2>Cercetarea pieței</h2>
            <h3>Surse de informații</h3>
            <ul>
                <li>Site-uri de joburi (Glassdoor, PayScale)</li>
                <li>Rapoarte salariale din industrie</li>
                <li>Networking cu profesioniști din domeniu</li>
                <li>Consultanți în resurse umane</li>
            </ul>
            
            <h2>Momentul potrivit</h2>
            <p>Cel mai bun moment pentru negociere este după ce ai primit oferta, dar înainte de a o accepta.</p>
            
            <h2>Strategii de negociere</h2>
            <h3>1. Prezintă valoarea ta</h3>
            <ul>
                <li>Evidențiază realizările anterioare</li>
                <li>Menționează competențele unice</li>
                <li>Demonstrează impactul pe care îl vei avea</li>
            </ul>
            
            <h3>2. Negociază pachetul complet</h3>
            <p>Nu te concentra doar pe salariul de bază:</p>
            <ul>
                <li>Bonusuri de performanță</li>
                <li>Beneficii medicale</li>
                <li>Zile libere suplimentare</li>
                <li>Opțiuni de lucru flexibil</li>
                <li>Oportunități de dezvoltare</li>
            </ul>
            
            <h3>3. Fii realist și flexibil</h3>
            <ul>
                <li>Propune o gamă salarială, nu o sumă fixă</li>
                <li>Fii deschis la compromisuri</li>
                <li>Consideră perspectivele pe termen lung</li>
            </ul>
            
            <h2>Greșeli de evitat</h2>
            <ul>
                <li>Nu negocia înainte de a primi oferta</li>
                <li>Nu compara cu salarii din alte industrii</li>
                <li>Nu fii agresiv sau ultimativ</li>
                <li>Nu uita să mulțumești pentru ofertă</li>
            </ul>
            ''',
            'is_featured': False
        },
        {
            'title': 'Tendințele pieței muncii în 2025',
            'excerpt': 'Analiză completă a tendințelor care vor defini piața muncii în următorul an.',
            'content': '''
            <h2>Transformarea pieței muncii</h2>
            <p>Anul 2025 aduce schimbări semnificative în modul în care lucrăm și în competențele căutate de angajatori.</p>
            
            <h2>1. Munca hibridă devine standard</h2>
            <p>Combinația între lucrul de acasă și de la birou se consolidează ca model preferat de majoritatea companiilor și angajaților.</p>
            
            <h2>2. Inteligența artificială în HR</h2>
            <ul>
                <li>Screening automatizat al CV-urilor</li>
                <li>Interviuri cu chatbots AI</li>
                <li>Analiză predictivă pentru retenția angajaților</li>
                <li>Personalizarea experiențelor de învățare</li>
            </ul>
            
            <h2>3. Competențele verzi</h2>
            <p>Sustenabilitatea devine prioritate, creând cerere pentru:</p>
            <ul>
                <li>Specialiști în energie regenerabilă</li>
                <li>Consultanți în sustenabilitate</li>
                <li>Ingineri pentru tehnologii verzi</li>
                <li>Analiști de impact ambiental</li>
            </ul>
            
            <h2>4. Upskilling și reskilling</h2>
            <p>Companiile investesc masiv în reconversia profesională a angajaților pentru a ține pasul cu tehnologia.</p>
            
            <h2>5. Wellbeing-ul angajaților</h2>
            <ul>
                <li>Programe de sănătate mentală</li>
                <li>Flexibilitate în programul de lucru</li>
                <li>Spații de lucru ergonomice</li>
                <li>Beneficii personalizate</li>
            </ul>
            
            <h2>6. Diversitatea și incluziunea</h2>
            <p>Companiile pun accent crescut pe crearea unor echipe diverse și inclusive.</p>
            
            <h2>7. Gig economy în expansiune</h2>
            <p>Munca pe proiecte și freelancing-ul continuă să crească, oferind flexibilitate atât angajatorilor, cât și lucrătorilor.</p>
            
            <h2>Pregătirea pentru viitor</h2>
            <ul>
                <li>Dezvoltă competențe digitale</li>
                <li>Investește în învățarea continuă</li>
                <li>Construiește o rețea profesională solidă</li>
                <li>Adaptează-te la schimbări</li>
            </ul>
            ''',
            'is_featured': True
        },
        {
            'title': 'Echilibrul între viața profesională și personală',
            'excerpt': 'Strategii practice pentru menținerea unui echilibru sănătos între carieră și viața personală.',
            'content': '''
            <h2>Importanța echilibrului work-life</h2>
            <p>Un echilibru sănătos între viața profesională și personală nu este doar un trend, ci o necesitate pentru bunăstarea pe termen lung.</p>
            
            <h2>Semnele unui dezechilibru</h2>
            <ul>
                <li>Oboseală cronică</li>
                <li>Stres constant</li>
                <li>Neglijarea relațiilor personale</li>
                <li>Scăderea productivității</li>
                <li>Probleme de sănătate</li>
            </ul>
            
            <h2>Strategii pentru echilibru</h2>
            <h3>1. Stabilește limite clare</h3>
            <ul>
                <li>Definește orele de lucru</li>
                <li>Nu verifica email-urile după program</li>
                <li>Comunică limitele tale echipei</li>
                <li>Învață să spui "nu" când este necesar</li>
            </ul>
            
            <h3>2. Prioritizează și organizează</h3>
            <ul>
                <li>Folosește tehnici de time management</li>
                <li>Delegă responsabilitățile</li>
                <li>Concentrează-te pe taskurile importante</li>
                <li>Planifică pauzele și vacanțele</li>
            </ul>
            
            <h3>3. Investește în relații</h3>
            <ul>
                <li>Petrece timp de calitate cu familia</li>
                <li>Menține prieteniile</li>
                <li>Participă la activități sociale</li>
                <li>Dezvoltă hobby-uri</li>
            </ul>
            
            <h3>4. Îngrijește-te de sănătate</h3>
            <ul>
                <li>Exerciții fizice regulate</li>
                <li>Alimentație echilibrată</li>
                <li>Somn suficient</li>
                <li>Practici de relaxare</li>
            </ul>
            
            <h2>Rolul angajatorului</h2>
            <p>Companiile progresiste oferă:</p>
            <ul>
                <li>Program flexibil de lucru</li>
                <li>Opțiuni de work from home</li>
                <li>Zile libere pentru sănătate mentală</li>
                <li>Programe de wellness</li>
                <li>Sprijin pentru dezvoltarea personală</li>
            </ul>
            
            <h2>Beneficiile echilibrului</h2>
            <ul>
                <li>Productivitate crescută</li>
                <li>Creativitate îmbunătățită</li>
                <li>Satisfacție profesională</li>
                <li>Relații mai bune</li>
                <li>Sănătate fizică și mentală</li>
            </ul>
            ''',
            'is_featured': False
        },
        {
            'title': 'Networking-ul eficient în carieră',
            'excerpt': 'Cum să construiești și să menții o rețea profesională puternică care să îți accelereze cariera.',
            'content': '''
            <h2>Puterea networking-ului</h2>
            <p>Studiile arată că 85% din joburi se obțin prin networking. O rețea profesională solidă poate deschide uși către oportunități neașteptate.</p>
            
            <h2>Tipuri de networking</h2>
            <h3>1. Networking intern</h3>
            <ul>
                <li>Colegi din departamente diferite</li>
                <li>Manageri și lideri</li>
                <li>Mentori interni</li>
                <li>Participanți la training-uri</li>
            </ul>
            
            <h3>2. Networking extern</h3>
            <ul>
                <li>Conferințe și evenimente din industrie</li>
                <li>Asociații profesionale</li>
                <li>Alumni universitari</li>
                <li>Platforme online (LinkedIn)</li>
            </ul>
            
            <h2>Strategii de networking</h2>
            <h3>1. Fii autentic</h3>
            <ul>
                <li>Construiește relații genuine</li>
                <li>Arată interes real pentru ceilalți</li>
                <li>Oferă ajutor înainte de a cere</li>
                <li>Fii consistent în comunicare</li>
            </ul>
            
            <h3>2. Pregătește-te pentru evenimente</h3>
            <ul>
                <li>Cercetează participanții</li>
                <li>Pregătește un elevator pitch</li>
                <li>Stabilește obiective clare</li>
                <li>Adună cărți de vizită</li>
            </ul>
            
            <h3>3. Folosește tehnologia</h3>
            <ul>
                <li>Optimizează profilul LinkedIn</li>
                <li>Participă la grupuri online</li>
                <li>Publică conținut relevant</li>
                <li>Comentează și interacționează</li>
            </ul>
            
            <h2>Menținerea relațiilor</h2>
            <ul>
                <li>Follow-up în 24-48 de ore</li>
                <li>Trimite actualizări periodice</li>
                <li>Oferă resurse utile</li>
                <li>Invită la cafea sau lunch</li>
                <li>Felicită pentru realizări</li>
            </ul>
            
            <h2>Networking online vs offline</h2>
            <h3>Avantajele networking-ului online:</h3>
            <ul>
                <li>Acces global</li>
                <li>Costuri reduse</li>
                <li>Flexibilitate de timp</li>
                <li>Ușurința menținerii contactului</li>
            </ul>
            
            <h3>Avantajele networking-ului offline:</h3>
            <ul>
                <li>Conexiuni mai profunde</li>
                <li>Comunicare non-verbală</li>
                <li>Încredere crescută</li>
                <li>Experiențe memorabile</li>
            </ul>
            
            <h2>Greșeli comune</h2>
            <ul>
                <li>Networking doar când ai nevoie de job</li>
                <li>Focusarea doar pe persoanele influente</li>
                <li>Nu oferirea de ajutor celorlalți</li>
                <li>Neglijarea urmăririi contactelor</li>
            </ul>
            ''',
            'is_featured': False
        },
        {
            'title': 'Dezvoltarea competențelor de leadership',
            'excerpt': 'Ghid complet pentru dezvoltarea abilităților de lider și avansarea în carieră.',
            'content': '''
            <h2>Ce înseamnă să fii lider</h2>
            <p>Leadership-ul nu se referă doar la poziția ierarhică, ci la capacitatea de a inspira, motiva și ghida oamenii către obiective comune.</p>
            
            <h2>Competențele esențiale ale unui lider</h2>
            <h3>1. Comunicarea eficientă</h3>
            <ul>
                <li>Ascultare activă</li>
                <li>Claritate în mesaje</li>
                <li>Adaptarea stilului de comunicare</li>
                <li>Feedback constructiv</li>
            </ul>
            
            <h3>2. Inteligența emotională</h3>
            <ul>
                <li>Autocunoaștere</li>
                <li>Autocontrol</li>
                <li>Empatie</li>
                <li>Competențe sociale</li>
            </ul>
            
            <h3>3. Gândirea strategică</h3>
            <ul>
                <li>Viziune pe termen lung</li>
                <li>Analiza situațiilor complexe</li>
                <li>Luarea deciziilor</li>
                <li>Planificarea și organizarea</li>
            </ul>
            
            <h2>Stiluri de leadership</h2>
            <h3>1. Leadership transformațional</h3>
            <p>Inspiră și motivează echipa să depășească așteptările.</p>
            
            <h3>2. Leadership servant</h3>
            <p>Pune nevoile echipei pe primul loc și servește dezvoltarea acesteia.</p>
            
            <h3>3. Leadership autentic</h3>
            <p>Bazat pe valori personale și transparență.</p>
            
            <h3>4. Leadership situațional</h3>
            <p>Adaptează stilul în funcție de situație și echipă.</p>
            
            <h2>Dezvoltarea competențelor de leadership</h2>
            <h3>1. Educația formală</h3>
            <ul>
                <li>MBA sau programe executive</li>
                <li>Cursuri de leadership</li>
                <li>Certificări profesionale</li>
                <li>Workshop-uri și seminarii</li>
            </ul>
            
            <h3>2. Experiența practică</h3>
            <ul>
                <li>Proiecte de echipă</li>
                <li>Voluntariat</li>
                <li>Mentorat</li>
                <li>Roluri de responsabilitate</li>
            </ul>
            
            <h3>3. Dezvoltarea personală</h3>
            <ul>
                <li>Lectură specializată</li>
                <li>Coaching profesional</li>
                <li>Feedback 360 de grade</li>
                <li>Reflecție și auto-evaluare</li>
            </ul>
            
            <h2>Provocările liderilor moderni</h2>
            <ul>
                <li>Gestionarea echipelor diverse</li>
                <li>Leadership la distanță</li>
                <li>Adaptarea la schimbări rapide</li>
                <li>Echilibrarea stakeholder-ilor</li>
                <li>Sustenabilitatea și responsabilitatea socială</li>
            </ul>
            
            <h2>Măsurarea succesului în leadership</h2>
            <ul>
                <li>Performanța echipei</li>
                <li>Satisfacția angajaților</li>
                <li>Retenția talentelor</li>
                <li>Inovația și creativitatea</li>
                <li>Rezultatele financiare</li>
            </ul>
            ''',
            'is_featured': False
        },
        {
            'title': 'Reconversia profesională: Ghid pas cu pas',
            'excerpt': 'Cum să faci tranziția către o nouă carieră cu succes și încredere.',
            'content': '''
            <h2>De ce să consideri reconversia profesională</h2>
            <p>Reconversia profesională poate fi motivată de diverse factori: automatizarea, schimbările din industrie, dorința de dezvoltare sau nevoia de echilibru.</p>
            
            <h2>Semnele că ai nevoie de reconversie</h2>
            <ul>
                <li>Lipsa motivației la locul de muncă</li>
                <li>Industria în declin</li>
                <li>Dorința de noi provocări</li>
                <li>Nevoia de venituri mai mari</li>
                <li>Schimbarea priorităților personale</li>
            </ul>
            
            <h2>Pașii pentru reconversie</h2>
            <h3>1. Auto-evaluarea</h3>
            <ul>
                <li>Identifică valorile și interesele</li>
                <li>Evaluează competențele actuale</li>
                <li>Determină obiectivele de carieră</li>
                <li>Analizează resursele disponibile</li>
            </ul>
            
            <h3>2. Cercetarea opțiunilor</h3>
            <ul>
                <li>Explorează industrii în creștere</li>
                <li>Studiază cerințele joburilor</li>
                <li>Identifică gap-urile de competențe</li>
                <li>Vorbește cu profesioniști din domeniu</li>
            </ul>
            
            <h3>3. Planificarea tranziției</h3>
            <ul>
                <li>Stabilește un timeline realist</li>
                <li>Creează un plan financiar</li>
                <li>Identifică resursele de învățare</li>
                <li>Construiește o strategie de networking</li>
            </ul>
            
            <h2>Dezvoltarea competențelor noi</h2>
            <h3>Opțiuni de învățare</h3>
            <ul>
                <li>Cursuri online (Coursera, Udemy)</li>
                <li>Bootcamp-uri intensive</li>
                <li>Certificări profesionale</li>
                <li>Programe universitare</li>
                <li>Apprenticeship-uri</li>
            </ul>
            
            <h3>Competențe transferabile</h3>
            <ul>
                <li>Comunicare și prezentare</li>
                <li>Gestionarea proiectelor</li>
                <li>Analiza și rezolvarea problemelor</li>
                <li>Leadership și lucrul în echipă</li>
                <li>Adaptabilitatea</li>
            </ul>
            
            <h2>Strategii pentru tranziție</h2>
            <h3>1. Tranziția graduală</h3>
            <ul>
                <li>Freelancing în timpul liber</li>
                <li>Proiecte part-time</li>
                <li>Voluntariat în domeniul nou</li>
                <li>Shadowing profesioniști</li>
            </ul>
            
            <h3>2. Tranziția completă</h3>
            <ul>
                <li>Demisia și focusarea pe învățare</li>
                <li>Programe intensive de reconversie</li>
                <li>Internship-uri în domeniul nou</li>
                <li>Startup propriu</li>
            </ul>
            
            <h2>Provocările reconversiei</h2>
            <ul>
                <li>Incertitudinea financiară</li>
                <li>Competiția cu candidații cu experiență</li>
                <li>Sindromul impostorului</li>
                <li>Presiunea timpului</li>
                <li>Rezistența la schimbare</li>
            </ul>
            
            <h2>Sfaturi pentru succes</h2>
            <ul>
                <li>Începe cu pași mici</li>
                <li>Construiește o rețea în domeniul nou</li>
                <li>Fii răbdător cu procesul</li>
                <li>Celebrează progresele mici</li>
                <li>Rămâi flexibil și adaptabil</li>
            </ul>
            ''',
            'is_featured': False
        },
        {
            'title': 'Munca de acasă: Productivitate și eficiență',
            'excerpt': 'Strategii și sfaturi pentru a fi productiv și eficient când lucrezi de acasă.',
            'content': '''
            <h2>Noua realitate a muncii de acasă</h2>
            <p>Munca de acasă a devenit norma pentru multe industrii. Succesul în acest mediu necesită disciplină, organizare și strategii specifice.</p>
            
            <h2>Amenajarea spațiului de lucru</h2>
            <h3>1. Spațiul dedicat</h3>
            <ul>
                <li>Desemnează o zonă exclusiv pentru lucru</li>
                <li>Investește într-un scaun ergonomic</li>
                <li>Asigură iluminare adecvată</li>
                <li>Minimizează distragerile</li>
            </ul>
            
            <h3>2. Tehnologia necesară</h3>
            <ul>
                <li>Computer performant</li>
                <li>Conexiune internet stabilă</li>
                <li>Căști cu microfon de calitate</li>
                <li>Monitor suplimentar</li>
                <li>Software de colaborare</li>
            </ul>
            
            <h2>Gestionarea timpului</h2>
            <h3>1. Rutina zilnică</h3>
            <ul>
                <li>Trezirea la aceeași oră</li>
                <li>Ritual de început al zilei</li>
                <li>Îmbrăcarea pentru lucru</li>
                <li>Pauze programate</li>
                <li>Încheierea clară a zilei de lucru</li>
            </ul>
            
            <h3>2. Tehnici de productivitate</h3>
            <ul>
                <li>Tehnica Pomodoro</li>
                <li>Time blocking</li>
                <li>Lista de priorități</li>
                <li>Eliminarea multitasking-ului</li>
            </ul>
            
            <h2>Comunicarea eficientă</h2>
            <h3>1. Meetinguri virtuale</h3>
            <ul>
                <li>Pregătește agenda în avans</li>
                <li>Testează tehnologia înainte</li>
                <li>Folosește funcția mute când nu vorbești</li>
                <li>Participă activ la discuții</li>
            </ul>
            
            <h3>2. Colaborarea online</h3>
            <ul>
                <li>Folosește platforme de colaborare</li>
                <li>Documentează deciziile importante</li>
                <li>Comunică proactiv cu echipa</li>
                <li>Stabilește expectații clare</li>
            </ul>
            
            <h2>Menținerea echilibrului</h2>
            <h3>1. Separarea vieții profesionale de cea personală</h3>
            <ul>
                <li>Stabilește ore fixe de lucru</li>
                <li>Creează ritualuri de început și sfârșit</li>
                <li>Evită lucrul în dormitor</li>
                <li>Comunică limitele familiei</li>
            </ul>
            
            <h3>2. Îngrijirea sănătății</h3>
            <ul>
                <li>Pauze regulate pentru mișcare</li>
                <li>Exerciții de stretching</li>
                <li>Hidratare adecvată</li>
                <li>Mese regulate și sănătoase</li>
            </ul>
            
            <h2>Provocările muncii de acasă</h2>
            <ul>
                <li>Izolarea socială</li>
                <li>Distragerile domestice</li>
                <li>Dificultatea separării muncii de viața personală</li>
                <li>Comunicarea redusă cu echipa</li>
                <li>Lipsa motivației</li>
            </ul>
            
            <h2>Soluții pentru provocări</h2>
            <ul>
                <li>Programează întâlniri virtuale informale</li>
                <li>Folosește aplicații pentru blocarea distragerilor</li>
                <li>Creează rutine clare</li>
                <li>Participă la evenimente de team building online</li>
                <li>Stabilește obiective zilnice</li>
            </ul>
            
            <h2>Viitorul muncii de acasă</h2>
            <p>Munca hibridă pare să fie viitorul, combinând beneficiile muncii de acasă cu avantajele interacțiunii față în față din birou.</p>
            ''',
            'is_featured': True
        }
    ]
    
    created_count = 0
    for article_data in articles_data:
        try:
            # Verifică dacă articolul există deja
            if not Article.objects.filter(title=article_data['title']).exists():
                article = Article.objects.create(
                    title=article_data['title'],
                    excerpt=article_data['excerpt'],
                    content=article_data['content'],
                    author=admin_user,
                    is_published=True,
                    is_featured=article_data['is_featured'],
                    published_at=timezone.now() - timedelta(days=created_count)
                )
                created_count += 1
                print(f"✅ Articol creat: {article.title}")
            else:
                print(f"⚠️ Articolul '{article_data['title']}' există deja")
        except Exception as e:
            print(f"❌ Eroare la crearea articolului '{article_data['title']}': {e}")
    
    print(f"\n🎉 Procesul s-a finalizat! Au fost create {created_count} articole noi.")
    print(f"📊 Total articole în baza de date: {Article.objects.count()}")

if __name__ == '__main__':
    create_articles()