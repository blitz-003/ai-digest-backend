import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.article import Article
from app.models.profile import Profile
from app.models.category import Category



ARTICLES = [

    {
        "title": "The Rise of AI Agents: How Autonomous Systems Are Changing Software",
        "slug": "rise-of-ai-agents-autonomous-systems",
        "summary": (
            "AI agents are becoming the next major evolution "
            "of artificial intelligence by combining reasoning, "
            "planning, and tool usage."
        ),
        "content": """
Artificial intelligence is moving beyond simple chat interfaces.

The next generation of AI systems are autonomous agents capable of understanding goals, planning tasks, using external tools, and improving workflows.

Companies are now building AI agents for software development, research, customer support, and business automation.

Unlike traditional AI models, agents can break complex problems into smaller steps and execute actions with minimal human intervention.

The future of software will likely involve humans collaborating with intelligent agents rather than manually completing every task.
        """,
        "reading_time": 5,
        "view_count": 120,
        "is_featured": True,
    },


    {
        "title": "Large Language Models Explained: From Transformers to GPT",
        "slug": "large-language-models-explained-transformers-gpt",
        "summary": (
            "A practical explanation of how modern large language models work."
        ),
        "content": """
Large Language Models power many modern AI applications.

These models are based on transformer architectures introduced in 2017.

Transformers allow models to understand relationships between words through attention mechanisms.

During training, billions of examples help models learn patterns in language, reasoning, and knowledge representation.

Today, LLMs are used in coding assistants, search engines, education platforms, and enterprise automation.
        """,
        "reading_time": 7,
        "view_count": 340,
        "is_featured": True,
    },


    {
        "title": "Machine Learning Trends Developers Should Watch in 2026",
        "slug": "machine-learning-trends-developers-2026",
        "summary": (
            "Important machine learning trends shaping the future of engineering."
        ),
        "content": """
Machine learning continues to evolve rapidly.

Developers should pay attention to several important trends:

- Smaller efficient AI models
- On-device machine learning
- AI infrastructure optimization
- Retrieval augmented generation
- Multimodal systems

Understanding these areas will become increasingly valuable for software engineers.
        """,
        "reading_time": 4,
        "view_count": 210,
        "is_featured": False,
    },


    {
        "title": "Building Production AI Applications With FastAPI and Next.js",
        "slug": "production-ai-applications-fastapi-nextjs",
        "summary": (
            "How modern full stack applications combine AI backends and frontend systems."
        ),
        "content": """
Building AI products requires more than calling an AI API.

Production systems need authentication, databases, background jobs, monitoring, and scalable infrastructure.

FastAPI provides a powerful backend framework for AI services, while Next.js offers a modern frontend experience.

Together they create a strong foundation for building reliable AI platforms.
        """,
        "reading_time": 6,
        "view_count": 95,
        "is_featured": False,
    },

]



def seed_articles():

    db: Session = SessionLocal()


    try:

        existing_articles = db.query(Article).count()

        if existing_articles > 0:
            print(
                "Articles already exist. Skipping."
            )
            return



        author = (
            db.query(Profile)
            .filter(
                Profile.role.in_(
                    [
                        "author",
                        "admin"
                    ]
                )
            )
            .first()
        )


        if not author:

            raise Exception(
                "No author/admin profile found. Create an author first."
            )



        categories = (
            db.query(Category)
            .all()
        )


        if not categories:

            raise Exception(
                "No categories found. Create categories first."
            )



        for index, article_data in enumerate(ARTICLES):

            article = Article(

                **article_data,

                status="published",

                published_at=datetime.now(
                    timezone.utc
                ),

                cover_image=(
                    "https://images.unsplash.com/"
                    "photo-1677442136019-21780ecad995"
                ),

                author_id=author.id,

                category_id=(
                    categories[
                        index % len(categories)
                    ].id
                ),

            )


            db.add(article)



        db.commit()


        print(
            f"✅ Created {len(ARTICLES)} real AI articles"
        )


    except Exception as e:

        db.rollback()

        print(
            "❌ Error:",
            e
        )


    finally:

        db.close()



if __name__ == "__main__":

    seed_articles()