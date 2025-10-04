#!/usr/bin/env python3
"""
Context Manager for Meteorite Madness Project
Manages project context, updates statistics, and tracks progress
"""

import json
import os
from datetime import datetime
from pathlib import Path
import subprocess

class ProjectContextManager:
    """Manages project context and tracking"""
    
    def __init__(self, context_file="context.json"):
        self.context_file = Path(context_file)
        self.context = self.load_context()
    
    def load_context(self):
        """Load context from JSON file"""
        try:
            with open(self.context_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Context file {self.context_file} not found!")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing context file: {e}")
            return {}
    
    def save_context(self):
        """Save context to JSON file"""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(self.context, f, indent=2, ensure_ascii=False)
            print(f"💾 Context saved to {self.context_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving context: {e}")
            return False
    
    def update_analysis_results(self, analysis_data):
        """Update analysis results in context"""
        if "analysis_results" not in self.context:
            self.context["analysis_results"] = {}
        
        self.context["analysis_results"]["latest_analysis"] = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            **analysis_data
        }
        
        # Update last modified timestamp
        self.context["project_info"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        
        print("📊 Analysis results updated in context")
    
    def add_visualization(self, viz_name, viz_type, description):
        """Add new visualization to context"""
        if "visualizations" not in self.context:
            self.context["visualizations"] = {"generated_files": {}}
        
        if viz_type not in self.context["visualizations"]["generated_files"]:
            self.context["visualizations"]["generated_files"][viz_type] = []
        
        viz_entry = {
            "name": viz_name,
            "description": description,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.context["visualizations"]["generated_files"][viz_type].append(viz_entry)
        print(f"🎨 Added visualization: {viz_name}")
    
    def update_file_statistics(self):
        """Update file and code statistics"""
        try:
            # Count Python files and lines
            python_files = list(Path(".").glob("*.py"))
            total_lines = 0
            
            for file in python_files:
                try:
                    with open(file, 'r') as f:
                        total_lines += len(f.readlines())
                except:
                    pass
            
            # Count all project files
            all_files = [f for f in Path(".").iterdir() 
                        if f.is_file() and not f.name.startswith('.') 
                        and f.name not in ['__pycache__']]
            
            # Update statistics
            if "performance_metrics" not in self.context:
                self.context["performance_metrics"] = {}
            
            self.context["performance_metrics"]["code_statistics"] = {
                "python_files": len(python_files),
                "total_files": len(all_files),
                "python_lines": total_lines,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"📈 Updated statistics: {len(python_files)} Python files, {total_lines} lines")
            
        except Exception as e:
            print(f"⚠️  Could not update file statistics: {e}")
    
    def get_project_summary(self):
        """Generate project summary"""
        summary = {
            "project": self.context.get("project_info", {}).get("name", "Unknown"),
            "version": self.context.get("project_info", {}).get("version", "Unknown"),
            "status": self.context.get("project_info", {}).get("status", "Unknown"),
            "last_analysis": self.context.get("analysis_results", {}).get("latest_analysis", {}).get("date", "Never"),
            "total_asteroids": self.context.get("analysis_results", {}).get("latest_analysis", {}).get("total_asteroids", 0),
            "data_sources": len(self.context.get("data_sources", {}).get("primary", {})),
            "visualizations": len(self.context.get("visualizations", {}).get("generated_files", {}))
        }
        return summary
    
    def add_milestone(self, milestone_name, description, deliverables=None):
        """Add project milestone"""
        if "project_timeline" not in self.context:
            self.context["project_timeline"] = {}
        
        milestone_key = f"milestone_{len(self.context['project_timeline']) + 1}"
        
        self.context["project_timeline"][milestone_key] = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "milestone": milestone_name,
            "description": description,
            "deliverables": deliverables or []
        }
        
        print(f"🎯 Added milestone: {milestone_name}")
    
    def generate_report(self):
        """Generate comprehensive project report"""
        summary = self.get_project_summary()
        
        report = f"""
🌌 METEORITE MADNESS PROJECT REPORT
{'='*50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 PROJECT OVERVIEW:
   • Name: {summary['project']}
   • Version: {summary['version']}
   • Status: {summary['status']}
   • Last Analysis: {summary['last_analysis']}

📈 KEY METRICS:
   • Asteroids Analyzed: {summary['total_asteroids']}
   • Data Sources: {summary['data_sources']}
   • Visualizations: {summary['visualizations']}

🔍 LATEST FINDINGS:
"""
        
        # Add latest analysis results
        if "analysis_results" in self.context and "latest_analysis" in self.context["analysis_results"]:
            analysis = self.context["analysis_results"]["latest_analysis"]
            report += f"   • Date Range: {analysis.get('date_range', 'Unknown')}\n"
            report += f"   • Potentially Hazardous: {analysis.get('potentially_hazardous', 0)} ({analysis.get('hazardous_percentage', 0)}%)\n"
            
            if "statistics" in analysis:
                stats = analysis["statistics"]
                if "distance" in stats:
                    report += f"   • Closest Approach: {stats['distance'].get('closest_approach_km', 0):,} km\n"
                if "size" in stats:
                    report += f"   • Largest Asteroid: {stats['size'].get('largest_diameter_km', 0)} km\n"
        
        # Add key findings
        if "analysis_results" in self.context and "key_findings" in self.context["analysis_results"]:
            report += "\n💡 KEY INSIGHTS:\n"
            for i, finding in enumerate(self.context["analysis_results"]["key_findings"][:5], 1):
                report += f"   {i}. {finding}\n"
        
        report += f"\n{'='*50}\n"
        
        return report
    
    def export_context(self, format="json"):
        """Export context in different formats"""
        if format == "json":
            export_file = f"context_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(export_file, 'w') as f:
                json.dump(self.context, f, indent=2, ensure_ascii=False)
            print(f"📤 Context exported to {export_file}")
            return export_file
        
        elif format == "summary":
            summary_file = f"project_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(summary_file, 'w') as f:
                f.write(self.generate_report())
            print(f"📤 Summary exported to {summary_file}")
            return summary_file
    
    def validate_context(self):
        """Validate context structure and data"""
        required_sections = [
            "project_info", "data_sources", "analysis_results", 
            "technical_architecture", "visualizations"
        ]
        
        issues = []
        
        for section in required_sections:
            if section not in self.context:
                issues.append(f"Missing section: {section}")
        
        # Check for empty critical data
        if "analysis_results" in self.context:
            if not self.context["analysis_results"].get("latest_analysis"):
                issues.append("No latest analysis data found")
        
        if issues:
            print("⚠️  Context validation issues:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        else:
            print("✅ Context validation passed")
            return True

def main():
    """Main function for context management operations"""
    print("🌌 Meteorite Madness Context Manager")
    print("="*40)
    
    manager = ProjectContextManager()
    
    # Update file statistics
    manager.update_file_statistics()
    
    # Validate context
    manager.validate_context()
    
    # Generate and display report
    report = manager.generate_report()
    print(report)
    
    # Save updated context
    manager.save_context()
    
    # Export summary
    manager.export_context("summary")
    
    print("✨ Context management complete!")

if __name__ == "__main__":
    main()
