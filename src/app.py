"""
Gradio app entrypoint for JingleTube karaoke application.

This module provides the web interface and core functionality for the JingleTube
karaoke application, including song management, score registration, and rankings.
"""

import gradio as gr
from typing import List, Tuple, Dict
from datetime import datetime


# In-memory storage for songs and scores
songs_database: Dict[str, Dict] = {}
scores_database: List[Dict] = []


def add_song(title: str, artist: str, file_path: str) -> Tuple[str, str]:
    """
    Add a new song to the karaoke library.
    
    Args:
        title: Song title
        artist: Artist name
        file_path: Path to the audio file
        
    Returns:
        Tuple of (success_message, error_message)
    """
    try:
        if not title or not artist:
            return "", "Error: Title and Artist are required"
        
        song_id = f"{artist}_{title}".replace(" ", "_").lower()
        
        if song_id in songs_database:
            return "", f"Error: Song '{title}' by {artist} already exists"
        
        songs_database[song_id] = {
            "title": title,
            "artist": artist,
            "file_path": file_path,
            "added_at": datetime.now().isoformat()
        }
        
        return f"✓ Successfully added '{title}' by {artist}", ""
    except Exception as e:
        return "", f"Error adding song: {str(e)}"


def register_score(player_name: str, song_title: str, score: int, notes_hit: int, notes_total: int) -> Tuple[str, str]:
    """
    Register a karaoke performance score.
    
    Args:
        player_name: Name of the player
        song_title: Title of the song performed
        score: Total score achieved
        notes_hit: Number of notes hit correctly
        notes_total: Total number of notes in the song
        
    Returns:
        Tuple of (success_message, error_message)
    """
    try:
        if not player_name or not song_title:
            return "", "Error: Player name and song title are required"
        
        if score < 0 or notes_hit < 0 or notes_total <= 0:
            return "", "Error: Invalid score values"
        
        accuracy = (notes_hit / notes_total * 100) if notes_total > 0 else 0
        
        score_record = {
            "player": player_name,
            "song": song_title,
            "score": score,
            "accuracy": accuracy,
            "notes_hit": notes_hit,
            "notes_total": notes_total,
            "timestamp": datetime.now().isoformat()
        }
        
        scores_database.append(score_record)
        
        return f"✓ Score registered for {player_name}: {score} points ({accuracy:.1f}% accuracy)", ""
    except Exception as e:
        return "", f"Error registering score: {str(e)}"


def get_rankings(limit: int = 10) -> str:
    """
    Get the top rankings based on scores.
    
    Args:
        limit: Number of top rankings to return
        
    Returns:
        Formatted string of rankings
    """
    try:
        if not scores_database:
            return "No scores registered yet. Be the first to sing!"
        
        # Sort by score in descending order
        sorted_scores = sorted(scores_database, key=lambda x: x["score"], reverse=True)
        top_scores = sorted_scores[:limit]
        
        rankings = "🏆 JingleTube Karaoke Rankings 🏆\n"
        rankings += "=" * 50 + "\n\n"
        
        for rank, record in enumerate(top_scores, 1):
            rankings += f"{rank}. {record['player']}\n"
            rankings += f"   Song: {record['song']}\n"
            rankings += f"   Score: {record['score']} points\n"
            rankings += f"   Accuracy: {record['accuracy']:.1f}%\n"
            rankings += f"   Notes: {record['notes_hit']}/{record['notes_total']}\n\n"
        
        return rankings
    except Exception as e:
        return f"Error retrieving rankings: {str(e)}"


def create_web_interface() -> gr.Blocks:
    """
    Create and configure the Gradio web interface for JingleTube.
    
    Returns:
        Configured Gradio Blocks interface
    """
    with gr.Blocks(title="JingleTube - Karaoke Application") as interface:
        gr.Markdown("# 🎤 JingleTube Karaoke Application")
        gr.Markdown("Sing, score, and compete with friends!")
        
        with gr.Tabs():
            # Add Song Tab
            with gr.TabItem("Add Song"):
                gr.Markdown("### Add a new song to the library")
                with gr.Row():
                    title_input = gr.Textbox(label="Song Title", placeholder="Enter song title")
                    artist_input = gr.Textbox(label="Artist", placeholder="Enter artist name")
                
                file_input = gr.File(label="Upload Audio File", type="filepath")
                
                with gr.Row():
                    add_button = gr.Button("Add Song", variant="primary")
                    success_msg = gr.Textbox(label="Status", interactive=False)
                    error_msg = gr.Textbox(label="Error", interactive=False)
                
                add_button.click(
                    fn=add_song,
                    inputs=[title_input, artist_input, file_input],
                    outputs=[success_msg, error_msg]
                )
            
            # Register Score Tab
            with gr.TabItem("Register Score"):
                gr.Markdown("### Register your performance score")
                with gr.Row():
                    player_input = gr.Textbox(label="Player Name", placeholder="Enter your name")
                    song_input = gr.Textbox(label="Song Title", placeholder="Enter song title")
                
                with gr.Row():
                    score_input = gr.Number(label="Score", value=0, precision=0)
                    notes_hit_input = gr.Number(label="Notes Hit", value=0, precision=0)
                    notes_total_input = gr.Number(label="Total Notes", value=1, precision=0)
                
                with gr.Row():
                    register_button = gr.Button("Register Score", variant="primary")
                    success_msg = gr.Textbox(label="Status", interactive=False)
                    error_msg = gr.Textbox(label="Error", interactive=False)
                
                register_button.click(
                    fn=register_score,
                    inputs=[player_input, song_input, score_input, notes_hit_input, notes_total_input],
                    outputs=[success_msg, error_msg]
                )
            
            # Rankings Tab
            with gr.TabItem("Rankings"):
                gr.Markdown("### Top Performers")
                with gr.Row():
                    limit_input = gr.Slider(label="Number of Rankings", value=10, minimum=1, maximum=50, step=1)
                    refresh_button = gr.Button("Refresh Rankings", variant="primary")
                
                rankings_output = gr.Textbox(label="Rankings", lines=20, interactive=False)
                
                refresh_button.click(
                    fn=get_rankings,
                    inputs=[limit_input],
                    outputs=[rankings_output]
                )
                
                # Auto-load rankings on tab open
                interface.load(
                    fn=get_rankings,
                    inputs=[limit_input],
                    outputs=[rankings_output]
                )
    
    return interface


def main():
    """Launch the JingleTube karaoke application."""
    app = create_web_interface()
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
