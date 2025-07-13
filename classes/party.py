"""
party.py - Manages a group of people traveling together on the Oregon Trail

This module handles party management, including:
- Adding/removing party members
- Daily health updates for the entire party
- Game over conditions (all members dead)
- Party-wide resource distribution
"""

from typing import List, Dict, Tuple
from classes.person import Person


class Party:
    """
    Manages a group of travelers on the Oregon Trail
    """
    
    def __init__(self, leader_name: str = "Player", leader_age: int = 30, leader_profession: str = "Farmer"):
        """
        Initialize party with a leader
        
        Args:
            leader_name: Name of party leader
            leader_age: Age of party leader  
            leader_profession: Profession of party leader
        """
        self.members: List[Person] = []
        self.leader = Person(leader_name, leader_age, leader_profession)
        self.members.append(self.leader)
        
        # Party statistics
        self.days_traveled = 0
        self.total_deaths = 0
        
        # Resource tracking
        self.food_reserves = 0.0  # pounds
        self.medicine_supplies = 0
        
    def add_member(self, name: str, age: int, profession: str = "Farmer") -> Person:
        """
        Add a new member to the party
        
        Args:
            name: Member's name
            age: Member's age
            profession: Member's profession
            
        Returns:
            The newly created Person object
        """
        new_member = Person(name, age, profession)
        self.members.append(new_member)
        return new_member
    
    def remove_member(self, person: Person):
        """Remove a member from the party (typically due to death)"""
        if person in self.members:
            self.members.remove(person)
            if not person.is_alive():
                self.total_deaths += 1
    
    def get_living_members(self) -> List[Person]:
        """Get all living party members"""
        return [member for member in self.members if member.is_alive()]
    
    def get_dead_members(self) -> List[Person]:
        """Get all deceased party members"""
        return [member for member in self.members if not member.is_alive()]
    
    def is_game_over(self) -> bool:
        """Check if all party members are dead (game over condition)"""
        return len(self.get_living_members()) == 0
    
    def get_party_status(self) -> Dict:
        """
        Get comprehensive party status
        
        Returns:
            Dictionary with party statistics and member status
        """
        living = self.get_living_members()
        dead = self.get_dead_members()
        
        # Calculate average health of living members
        avg_health = 0
        if living:
            total_health = sum(member.health for member in living)
            avg_health = total_health / len(living)
        
        # Get worst health status
        worst_health = 100
        worst_member = None
        for member in living:
            if member.health < worst_health:
                worst_health = member.health
                worst_member = member
        
        return {
            "total_members": len(self.members),
            "living_members": len(living),
            "dead_members": len(dead),
            "average_health": round(avg_health, 1),
            "worst_health": worst_health,
            "worst_member": worst_member.name if worst_member else None,
            "days_traveled": self.days_traveled,
            "total_deaths": self.total_deaths,
            "game_over": self.is_game_over()
        }
    
    def distribute_food(self, total_food_available: float, rationing_level: float = 1.0) -> Dict:
        """
        Distribute daily food among living party members
        
        Args:
            total_food_available: Total pounds of food available for the day
            rationing_level: Food rationing (0.5 = half rations, 1.0 = full, 1.5 = extra)
            
        Returns:
            Dictionary showing food distribution results
        """
        living_members = self.get_living_members()
        if not living_members:
            return {"success": False, "reason": "No living members"}
        
        # Calculate total food needed
        daily_requirement = 2.0  # pounds per person per day
        total_needed = len(living_members) * daily_requirement * rationing_level
        
        # Distribute food
        if total_food_available >= total_needed:
            # Enough food for everyone
            food_per_person = daily_requirement * rationing_level
            for member in living_members:
                member.daily_update(food_consumed=food_per_person)
            
            return {
                "success": True,
                "food_used": total_needed,
                "food_remaining": total_food_available - total_needed,
                "rations": "Full" if rationing_level >= 1.0 else "Reduced",
                "members_fed": len(living_members)
            }
        else:
            # Not enough food - distribute equally
            if total_food_available > 0:
                food_per_person = total_food_available / len(living_members)
                for member in living_members:
                    member.daily_update(food_consumed=food_per_person)
            else:
                # No food at all
                for member in living_members:
                    member.daily_update(food_consumed=0)
            
            return {
                "success": False,
                "food_used": total_food_available,
                "food_remaining": 0,
                "rations": "Starvation",
                "members_fed": len(living_members),
                "food_per_person": total_food_available / len(living_members) if living_members else 0
            }
    
    def apply_weather_to_party(self, weather: str, shelter_quality: float = 1.0):
        """
        Apply weather effects to all living party members
        
        Args:
            weather: Weather type (hot, cold, rain, snow, storm)
            shelter_quality: Quality of shelter (0.0 = no protection, 1.0 = full protection)
        """
        living_members = self.get_living_members()
        for member in living_members:
            member.apply_weather_exposure(weather, shelter_quality)
    
    def treat_sick_members(self, medicine_available: int) -> Dict:
        """
        Treat sick party members with available medicine
        
        Args:
            medicine_available: Number of medicine units available
            
        Returns:
            Dictionary showing treatment results
        """
        living_members = self.get_living_members()
        sick_members = []
        
        # Find members who need treatment (health < 50 or have conditions)
        for member in living_members:
            if member.health < 50 or len(member.health_system.conditions) > 1:
                sick_members.append(member)
        
        # Sort by health (worst first)
        sick_members.sort(key=lambda m: m.health)
        
        treatments_given = 0
        treated_members = []
        
        for member in sick_members:
            if treatments_given < medicine_available:
                member.apply_medicine("General Medicine", effectiveness=0.8)
                treated_members.append(member.name)
                treatments_given += 1
            else:
                break
        
        return {
            "medicine_used": treatments_given,
            "medicine_remaining": medicine_available - treatments_given,
            "members_treated": treated_members,
            "members_needing_treatment": len(sick_members),
            "untreated_members": len(sick_members) - treatments_given
        }
    
    def daily_party_update(self, 
                          food_available: float = 0, 
                          rationing_level: float = 1.0,
                          rest_hours: int = 8,
                          rest_quality: float = 1.0,
                          weather: str = "fair",
                          shelter_quality: float = 1.0,
                          medicine_used: int = 0) -> Dict:
        """
        Process a full day for the entire party
        
        Args:
            food_available: Pounds of food available for the day
            rationing_level: Food rationing level
            rest_hours: Hours of rest for the day
            rest_quality: Quality of rest
            weather: Weather conditions
            shelter_quality: Quality of shelter
            medicine_used: Medicine units used
            
        Returns:
            Comprehensive daily report
        """
        self.days_traveled += 1
        
        # Distribute food
        food_result = self.distribute_food(food_available, rationing_level)
        
        # Apply weather effects
        self.apply_weather_to_party(weather, shelter_quality)
        
        # Apply rest to all members (already done in food distribution for living members)
        living_members = self.get_living_members()
        for member in living_members:
            # Update rest separately since food distribution only handles food
            member.health_system.get_rest(rest_hours, rest_quality)
            member.health_system.daily_health_update()
            member.health = member.health_system.current_health
            member.status = "Dead" if not member.health_system.is_alive else "Alive"
        
        # Treat sick members
        treatment_result = self.treat_sick_members(medicine_used)
        
        # Remove dead members
        dead_today = []
        for member in self.members[:]:  # Copy list to avoid modification during iteration
            if not member.is_alive() and member.status == "Alive":
                dead_today.append(member.name)
                member.status = "Dead"
        
        # Compile daily report
        party_status = self.get_party_status()
        
        return {
            "day": self.days_traveled,
            "food_distribution": food_result,
            "treatment": treatment_result,
            "deaths_today": dead_today,
            "party_status": party_status,
            "weather": weather,
            "game_over": self.is_game_over()
        }
    
    def get_detailed_party_report(self) -> str:
        """Get a detailed text report of party status"""
        report = []
        report.append(f"=== PARTY STATUS - Day {self.days_traveled} ===")
        report.append("")
        
        living_members = self.get_living_members()
        dead_members = self.get_dead_members()
        
        if living_members:
            report.append("LIVING MEMBERS:")
            for member in living_members:
                report.append(f"  • {member}")
        
        if dead_members:
            report.append("")
            report.append("DECEASED MEMBERS:")
            for member in dead_members:
                report.append(f"  • {member.name} (Age {member.age}) - {member.profession}")
        
        report.append("")
        party_status = self.get_party_status()
        report.append(f"Average Health: {party_status['average_health']}/100")
        report.append(f"Total Deaths: {party_status['total_deaths']}")
        
        if self.is_game_over():
            report.append("")
            report.append("*** GAME OVER - ALL PARTY MEMBERS HAVE DIED ***")
        
        return "\n".join(report)
    
    def __str__(self):
        living = len(self.get_living_members())
        dead = len(self.get_dead_members())
        return f"Party: {living} living, {dead} dead (Day {self.days_traveled})"
