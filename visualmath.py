import streamlit as st
import numpy as np
import plotly.express as px
import sympy as sp

def cached_plot_equations(equations_x, equations_y):
    @st.cache_data
    def _plot_equations_cached(equations_x, equations_y):
        fig = px.line(x=np.linspace(-10, 10, 4000))
        fig.data=[]
        x, y = sp.symbols('x y')
        
        for eq in equations_x:
            try:
                parsed_eq = sp.sympify(eq)
                x_vals = np.linspace(-100, 100, 40000)
                y_vals = np.array([parsed_eq.subs(x, val) for val in x_vals], dtype=np.float32)
                fig.add_scatter(x=x_vals, y=y_vals, mode='lines', name=f'y = {eq}', line_shape='linear')
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        for eq in equations_y:
            try:
                parsed_eq = sp.sympify(eq)
                y_vals = np.linspace(-100, 100, 40000)
                x_vals = np.array([parsed_eq.subs(y, val) for val in y_vals], dtype=np.float32)
                fig.add_scatter(x=x_vals, y=y_vals, mode='lines', name=f'x = {eq}', line_shape='linear')
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        fig.update_layout(
            xaxis_title='x',
            yaxis_title='y',
            title='Graph of Equations',
            xaxis=dict(zeroline=False),
            yaxis=dict(zeroline=False),
            xaxis_range=[-10, 10],
            yaxis_range=[-10, 10],
        )
        
        return fig
    
    return _plot_equations_cached(equations_x, equations_y)

def main():
    st.title("Mathematical Equation Visualizer")
    
    equations_x = st.sidebar.text_area("Enter the equations in x (one per line)", help="Enter equations in a valid mathematical format, e.g., x**2 + 5*x + 6")
    equations_list_x = equations_x.split("\n") if equations_x else []
    
    plot_button_x = st.sidebar.button("Plot Equations in x")
    if plot_button_x:
        cached_plot_equations(equations_list_x, [])
    
    equations_y = st.sidebar.text_area("Enter the equations in y (one per line)", help="Enter equations in a valid mathematical format, e.g., y**2 + 5*y + 6")
    equations_list_y = equations_y.split("\n") if equations_y else []
    
    plot_button_y = st.sidebar.button("Plot Equations in y")
    if plot_button_y:
        cached_plot_equations([], equations_list_y)
    
    st.plotly_chart(cached_plot_equations(equations_list_x, equations_list_y), use_container_width=True)

if __name__ == "__main__":
    main()
