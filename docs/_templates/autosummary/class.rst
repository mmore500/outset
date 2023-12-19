{{ name | escape | underline }}

.. currentmodule:: ~{{ module }}

.. autoclass:: {{ fullname }}
   :undoc-members:
   :members:
   :special-members: __call__, __repr__, __str__

   {% block methods %}
   .. automethod:: __init__

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   {% for item in methods %}
   .. automethod:: ~{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
