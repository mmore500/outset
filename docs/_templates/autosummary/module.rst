{{ name | escape | underline }}

.. currentmodule:: ~{{ module }}

{% if modules != all_modules %}
.. automodule:: {{ fullname }}
   :undoc-members:
   :members:
   :imported-members:
   :special-members: __call__, __repr__, __str__
{% else %}
.. automodule:: {{ fullname }}
{% endif %}

   {% block modules %}

   {% if modules %}
   .. rubric:: Modules

   .. autosummary::
      :toctree:
      :recursive:
   {% for item in modules %}
      ~{{ item }}
   {%- endfor %}
   {% endif %}

   {% set ns = namespace(forwarded_modules = false) %}
   {% for item in members %}
   {% if item not in all_functions and item not in all_classes and item not in all_exceptions and item not in all_attributes and item not in all_modules and item not in modules and item not in " ".join(modules) and item not in " ".join(all_modules) %}
   {% if not item.startswith("_") %}
      {% set ns.forwarded_modules = true %}
   {% endif %}
   {% endif %}
   {%- endfor %}

   {% if ns.forwarded_modules %}

   .. rubric:: {{ _('Forwarded Modules') }}

   Modules defined elsewhere made available in this namespace for convenience.
   To view documentation for these modules, use the search bar or navigate to the source package manually.

   .. autosummary::
   {% for item in members %}
   {% if item not in all_functions and item not in all_classes and item not in all_exceptions and item not in all_attributes and item not in all_modules and item not in modules and item not in " ".join(modules) and item not in " ".join(all_modules) %}
   {% if not item.startswith("_") %}
      {{ item }}
   {% endif %}
   {% endif %}
   {%- endfor %}
   {% endif %}

   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Module Attributes') }}

   .. autosummary::
     :toctree:
   {% for item in attributes %}
      ~{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::
     :toctree:
   {% for item in functions %}
      ~{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
     :toctree:
   {% for item in classes %}
      ~{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::
     :toctree:
   {% for item in exceptions %}
      ~{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
