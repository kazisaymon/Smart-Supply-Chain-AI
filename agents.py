"""
CrewAI Agents - সাপ্লাই চেইন ম্যানেজমেন্ট
"""

from crewai import Agent, Task, Crew
from tools import EmailTool, DatabaseTool, TrackingTool, AnalyticsTool
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os

# Environment setup
email_tool = EmailTool()
db_tool = DatabaseTool()
tracking_tool = TrackingTool()
analytics_tool = AnalyticsTool()


# ============================================
# Agents Definition
# ============================================

class SupplyChainAgents:
    """সাপ্লাই চেইন ম্যানেজমেন্ট এজেন্ট"""

    @staticmethod
    def inventory_manager_agent():
        """ইনভেন্টরি ম্যানেজার এজেন্ট"""
        return Agent(
            role="ইনভেন্টরি ম্যানেজার",
            goal="ইনভেন্টরি লেভেল অপ্টিমাইজ করা এবং স্টক-আউট প্রতিরোধ করা",
            backstory="""আপনি একজন অভিজ্ঞ ইনভেন্টরি ম্যানেজার যিনি সাপ্লাই চেইন দক্ষতার উপর ফোকাস করেন। 
            আপনি ডেটা-ড্রিভেন সিদ্ধান্ত নেন এবং স্বয়ংক্রিয় অর্ডার ট্রিগার করেন।""",
            verbose=True,
            allow_delegation=False
        )

    @staticmethod
    def procurement_agent():
        """প্রকিউরমেন্ট এজেন্ট"""
        return Agent(
            role="প্রকিউরমেন্ট স্পেশালিস্ট",
            goal="সেরা দামে সাপ্লায়ারদের সাথে অর্ডার প্লেস করা",
            backstory="""আপনি একজন অভিজ্ঞ ক্রয় পেশাদার যিনি সাপ্লায়ার সম্পর্ক পরিচালনা করেন।
            আপনি খরচ দক্ষতা এবং গুণমান নিশ্চিত করেন।""",
            verbose=True,
            allow_delegation=False
        )

    @staticmethod
    def logistics_agent():
        """লজিস্টিক্স এজেন্ট"""
        return Agent(
            role="লজিস্টিক্স কোঅর্ডিনেটর",
            goal="অর্ডার ডেলিভারি ট্র্যাক করা এবং বিলম্ব হ্যান্ডেল করা",
            backstory="""আপনি একজন লজিস্টিক বিশেষজ্ঞ যিনি সময়মত ডেলিভারি নিশ্চিত করেন।
            আপনি সম্ভাব্য সমস্যাগুলি সনাক্ত করেন এবং প্রশমন কৌশল তৈরি করেন।""",
            verbose=True,
            allow_delegation=False
        )

    @staticmethod
    def analytics_agent():
        """বিশ্লেষণ এজেন্ট"""
        return Agent(
            role="ডেটা বিশ্লেষক",
            goal="সাপ্লাই চেইনের প্রবণতা এবং সুযোগ চিহ্নিত করা",
            backstory="""আপনি একজন ডেটা বিশ্লেষক যিনি প্যাটার্ন চিহ্নিত করেন এবং সুপারিশ করেন।
            আপনি ঐতিহাসিক ডেটা ব্যবহার করে ভবিষ্যতের চাহিদা পূর্বাভাস দেন।""",
            verbose=True,
            allow_delegation=False
        )


# ============================================
# Tasks Definition
# ============================================

class SupplyChainTasks:
    """সাপ্লাই চেইন টাস্ক"""

    @staticmethod
    def check_inventory_levels(agent, db: Session):
        """ইনভেন্টরি লেভেল চেক করুন"""
        return Task(
            description="""
            ইনভেন্টরি সিস্টেম চেক করুন এবং নিম্নলিখিত করুন:
            1. কম স্টক আইটেম চিহ্নিত করুন
            2. পুনরায় অর্ডার প্রয়োজনীয় পণ্য সুপারিশ করুন
            3. ইনভেন্টরি স্ট্যাটাস সারাংশ প্রদান করুন
            """,
            agent=agent,
            expected_output="ইনভেন্টরি স্ট্যাটাস রিপোর্ট এবং সুপারিশ"
        )

    @staticmethod
    def process_purchase_orders(agent, db: Session):
        """ক্রয় অর্ডার প্রক্রিয়া করুন"""
        return Task(
            description="""
            নিম্নলিখিত অর্ডার প্রক্রিয়া করুন:
            1. পেন্ডিং অর্ডার চিহ্নিত করুন
            2. সাপ্লায়ার যোগাযোগ ত্রুটি চেক করুন
            3. অর্ডার নিশ্চিতকরণ পাঠান
            4. প্রত্যাশিত ডেলিভারি তারিখ আপডেট করুন
            """,
            agent=agent,
            expected_output="প্রক্রিয়াকৃত অর্ডারের তালিকা এবং স্ট্যাটাস"
        )

    @staticmethod
    def track_shipments(agent, db: Session):
        """চালান ট্র্যাক করুন"""
        return Task(
            description="""
            সব চলমান চালান ট্র্যাক করুন:
            1. বিলম্বিত অর্ডার চিহ্নিত করুন
            2. সম্ভাব্য সরবরাহ চেইন ব্যাঘাত সতর্ক করুন
            3. সাপ্লায়ারদের সাথে যোগাযোগ করুন
            4. সম্ভাব্য সমাধান প্রস্তাব করুন
            """,
            agent=agent,
            expected_output="ট্র্যাকিং স্ট্যাটাস এবং সুপারিশ"
        )

    @staticmethod
    def generate_analytics_report(agent, db: Session):
        """বিশ্লেষণ রিপোর্ট তৈরি করুন"""
        return Task(
            description="""
            সাপ্লাই চেইন বিশ্লেষণ রিপোর্ট তৈরি করুন:
            1. ইনভেন্টরি মূল্য ট্রেন্ড বিশ্লেষণ করুন
            2. সাপ্লায়ার পারফরম্যান্স মূল্যায়ন করুন
            3. খরচ সাশ্রয়ের সুযোগ চিহ্নিত করুন
            4. অপ্টিমাইজেশনের জন্য সুপারিশ প্রদান করুন
            """,
            agent=agent,
            expected_output="বিস্তৃত বিশ্লেষণ এবং কর্মক্ষম সুপারিশ"
        )


# ============================================
# Crew Setup
# ============================================

class SupplyChainCrew:
    """সাপ্লাই চেইন ক্রু অর্কেস্ট্রেশন"""

    def __init__(self, db: Session):
        self.db = db
        self.agents = SupplyChainAgents()
        self.tasks = SupplyChainTasks()

    def daily_operations_crew(self):
        """দৈনিক অপারেশন ক্রু"""
        agents = [
            self.agents.inventory_manager_agent(),
            self.agents.procurement_agent(),
            self.agents.logistics_agent()
        ]

        tasks = [
            self.tasks.check_inventory_levels(agents[0], self.db),
            self.tasks.process_purchase_orders(agents[1], self.db),
            self.tasks.track_shipments(agents[2], self.db)
        ]

        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True
        )

        return crew

    def weekly_analytics_crew(self):
        """সাপ্তাহিক বিশ্লেষণ ক্রু"""
        agent = self.agents.analytics_agent()
        task = self.tasks.generate_analytics_report(agent, self.db)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        return crew

    def run_daily_operations(self):
        """দৈনিক অপারেশন চালান"""
        print("\n🤖 দৈনিক সাপ্লাই চেইন অপারেশন শুরু করছি...")
        crew = self.daily_operations_crew()
        result = crew.kickoff()
        print("\n✅ দৈনিক অপারেশন সম্পন্ন")
        return result

    def run_weekly_analytics(self):
        """সাপ্তাহিক বিশ্লেষণ চালান"""
        print("\n📊 সাপ্তাহিক বিশ্লেষণ শুরু করছি...")
        crew = self.weekly_analytics_crew()
        result = crew.kickoff()
        print("\n✅ বিশ্লেষণ সম্পন্ন")
        return result


# ============================================
# Utility Functions
# ============================================

def run_supply_chain_agent(db: Session, operation_type: str = "daily"):
    """সাপ্লাই চেইন এজেন্ট চালান"""
    crew_manager = SupplyChainCrew(db)

    if operation_type == "daily":
        return crew_manager.run_daily_operations()
    elif operation_type == "weekly":
        return crew_manager.run_weekly_analytics()
    else:
        return {"error": "অজানা অপারেশন টাইপ"}


if __name__ == "__main__":
    print("✅ এজেন্ট মডিউল লোড করা হয়েছে")
